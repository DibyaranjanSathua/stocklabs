"""
File:           api.py
Author:         Dibyaranjan Sathua
Created on:     25/03/21, 7:00 pm

Get the API key from http://develop-api.aliceblueonline.com/
"""
from typing import Optional, Dict, List
import datetime
import logging
import requests
import websocket
from bs4 import BeautifulSoup

from alice_blue_api.config import Config
from alice_blue_api.exceptions import AliceBlueApiError
from alice_blue_api.instruments import Instruments
from alice_blue_api.enums import OptionType, Exchanges


class ApiEndpoint:
    """ Contains AliceBlue API endpoints """
    AUTHORIZE: str = "/oauth2/auth"
    ACCESS_TOKEN: str = "/oauth2/token"
    MASTER_CONTRACT: str = "/api/v2/contracts.json?exchanges={exchange}"


class AliceBlueApi:
    """ Class responsible for AliceBlue API """
    BASE_URL = "https://ant.aliceblueonline.com"

    def __init__(self):
        self._username: str = Config.USERNAME
        self._password: str = Config.PASSWORD
        self._app_id: str = Config.APPID
        self._app_secret: str = Config.APPSECRET
        self._redirect_url: str = Config.REDIRECT_URL
        self._2fa_answer: str = Config.TWO_FA_ANSWER
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        self._logger.addHandler(handler)
        self._headers = {
            "Content-Type": "application/json",
        }
        self._master_contracts = dict()
        self._options_master_contracts = []
        self._future_master_contracts = []
        self._bnf_instruments: List[Instruments] = []
        self._access_token: str = ""

    def api_setup(self):
        """ Setup APIs """
        self._access_token = self.generate_access_token()
        self._headers["Authorization"] = f"Bearer {self._access_token}"

    def generate_access_token(self):
        """ Get access token """
        session = requests.Session()
        url = f"{self.BASE_URL}{ApiEndpoint.AUTHORIZE}?response_type=code&" \
              f"state=test_state&client_id={self._app_id}&redirect_uri={self._redirect_url}"
        response = session.get(url)
        if "OAuth 2.0 Error" in response.text:
            self._logger.error(
                "OAuth 2.0 Error occurred. Please verify your app id and redirect url"
            )
        soup = BeautifulSoup(response.text, features="html.parser")
        csrf_token = soup.find("input", attrs={"name": "_csrf_token"})["value"]
        login_challenge = soup.find("input", attrs={"name": "login_challenge"})["value"]
        payload = {
            "client_id": self._username,
            "password": self._password,
            "login_challenge": login_challenge,
            "_csrf_token": csrf_token
        }
        response = session.post(response.url, data=payload)
        if "Please Enter Valid Password" in response.text:
            self._logger.error("Invalid password")

        if not response.ok:
            self._logger.error("Something went wrong at username password stage. "
                               "Not able to redirect to two factor authentication (2FA)")

        question_ids = []
        soup = BeautifulSoup(response.text, features="html.parser")
        for x in soup.find_all("input", attrs={"name": "question_id1"}):
            question_ids.append(x["value"])
        csrf_token = soup.find("input", attrs={"name": "_csrf_token"})["value"]
        login_challenge = soup.find("input", attrs={"name": "login_challenge"})["value"]
        payload = {
            "answer1": self._2fa_answer,
            "answer2": self._2fa_answer,
            "question_id1": question_ids,
            "login_challenge": login_challenge,
            "_csrf_token": csrf_token
        }
        response = session.post(response.url, data=payload)
        if "Wrong Answers" in response.text:
            self._logger.error("2FA answers are wrong. Make sure all your 2FA answers are same")

        if not response.ok:
            self._logger.error("Something went wrong at 2FA stage. Not able to get code.")

        # Authorizing app for the first time
        if "consent_challenge" in response.url:
            authorize_app_url = response.url
            self._logger.info("Authorizing app for the first time")
            soup = BeautifulSoup(response.text, features="html.parser")
            csrf_token = soup.find("input", attrs={"name": "_csrf_token"})["value"]
            payload = {
                "_csrf_token": csrf_token,
                "consent": "Authorize",
                "scopes": ""
            }
            response = session.post(response.url, data=payload)
            if not response.ok:
                self._logger.error(f"Something went wrong while authorizing the app for the first "
                                   f"time. Please authorize manually by going to URL "
                                   f"{authorize_app_url}")

        query_params_str = response.url.split("?")[1].split("&")
        query_params = {}
        for param in query_params_str:
            name, value = param.split("=")
            query_params[name] = value
        code = query_params["code"]
        self._logger.info(f"Code: {code}")
        # Get Access Token
        payload = {
            "code": code,
            "redirect_uri": self._redirect_url,
            "grant_type": "authorization_code"
        }
        url = f"{self.BASE_URL}{ApiEndpoint.ACCESS_TOKEN}"
        response = session.post(url, auth=(self._app_id, self._app_secret), data=payload)
        json_data = response.json()
        if "access_token" in json_data:
            access_token = json_data["access_token"]
            self._logger.info(f"Access Token: {access_token}")
            return access_token
        self._logger.error(f"Couldn't get access token {response.text}")

    def api_call(
            self,
            endpoint: str,
            method: str,
            query_params: Optional[Dict] = None,
            data: Optional[Dict] = None
    ):
        """ API call """
        url = f"{self.BASE_URL}{endpoint}"
        if query_params is not None:
            url = url.format(**query_params)
        kwargs = {"headers": self._headers}
        self._logger.debug(f"Sending {method.upper()} request to {url}")
        if method.upper() in ["GET"]:
            kwargs["params"] = data
        elif method.upper() in ["POST"]:
            kwargs["data"] = data
        response = requests.request(method=method.upper(), url=url, **kwargs)
        if not response.ok:
            self._logger.error(f"Non 200 status code from {url}")
            self._logger.error(response.text)
            raise AliceBlueApiError("Non 200 status code")
        return response.json()

    def option_setup(self):
        """ Get all the required master contracts """
        self.get_master_contracts(exchange=Exchanges.NFO.name)
        self._options_master_contracts = self._master_contracts["NSE-OPT"]
        self._future_master_contracts = self._master_contracts["NSE-FUT"]
        self.create_bnf_instruments()

    def get_master_contracts(self, exchange):
        """ Get all the tradable contracts of an exchange """
        self._master_contracts = self.api_call(
            endpoint=ApiEndpoint.MASTER_CONTRACT,
            method="GET",
            query_params={"exchange": exchange}
        )

    def create_bnf_instruments(self):
        """ Return list of bnf instruments from master contracts """
        self._bnf_instruments = [
            Instruments.create(x)
            for x in self._nfo_master_contracts if "BANKNIFTY" in x["symbol"]
        ]

    def get_bnf_option_instrument(
            self, strike: int, expiry: datetime.date, option_type: OptionType
    ):
        """ Get Call Option instrument by strike and expiry """
        return next(
            (
                x for x in self._bnf_instruments
                if x.option_type == option_type and x.strike == strike and x.expiry == expiry
            ),
            None
        )

    @property
    def bnf_instruments(self) -> List[Instruments]:
        return self._bnf_instruments

    @property
    def access_token(self) -> str:
        return self._access_token


if __name__ == "__main__":
    import json
    obj = AliceBlueApi()
    obj.api_setup()
    obj.option_setup()
    instrument = obj.get_bnf_instrument(
        strike=35000, expiry=datetime.date(2021, 7, 1), option_type=OptionType.CE
    )
    print(instrument)
    # with open("master_contracts.json", "w") as fh_:
    #     json.dump(bnf_contracts, fh_)

