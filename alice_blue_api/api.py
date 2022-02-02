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
from bs4 import BeautifulSoup
import json

from alice_blue_api.config import Config
from alice_blue_api.exceptions import AliceBlueApiError
from alice_blue_api.instruments import Instrument
from alice_blue_api.enums import OptionType, Exchanges


class ApiEndpoint:
    """ Contains AliceBlue API endpoints """
    AUTHORIZE: str = "/oauth2/auth"
    ACCESS_TOKEN: str = "/oauth2/token"
    MASTER_CONTRACT: str = "/api/v2/contracts.json?exchanges={exchange}"
    LOGIN: str = "/api/v1/user/login"
    TWO_FA: str = "/api/v1/user/twofa"


class AliceBlueApi:
    """ Class responsible for AliceBlue API. This is a singleton class """
    BASE_URL = "https://ant.aliceblueonline.com"
    __instance: Optional["AliceBlueApi"] = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(AliceBlueApi, cls).__new__(cls, *args, **kwargs)
            return cls.__instance
        raise SyntaxError("This is a Singleton class. Use get_handler() method")

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        self._logger.addHandler(handler)
        self._headers = {
            "Content-Type": "application/json",
        }
        self._master_contracts_nfo = dict()
        self._master_contracts_nse = dict()
        self._options_master_contracts = []
        self._future_master_contracts = []
        self._nse_indices_contracts = []
        self._nse_stock_contracts = []
        self._bnf_instruments: List[Instrument] = []
        self._nifty_instruments: List[Instrument] = []
        self._nifty_index: Optional[Instrument] = None
        self._banknifty_index: Optional[Instrument] = None
        self._india_vix_index: Optional[Instrument] = None
        self._access_token: str = ""
        self._auth_token: str = ""

    @classmethod
    def get_handler(cls):
        """ Get or create API handler """
        if cls.__instance is None:
            cls.__instance = AliceBlueApi()
        return cls.__instance

    @classmethod
    def reset(cls):
        """ Method for test purposes. Don't use it in real code """
        cls.__instance = None

    def api_setup(self):
        """ Setup APIs """
        self.refresh_access_token()
        # self.refresh_auth_token()
        self._headers["Authorization"] = f"Bearer {self._access_token}"

    def refresh_auth_token(self):
        """ Generate a new auth token """
        self._auth_token = self.generate_auth_token()

    def refresh_access_token(self):
        """ Generate a new access token """
        self._access_token = self.generate_access_token()

    def generate_auth_token(self):
        """ This token will be used for alice blue internal API such as to get candle data """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-IN,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
            "x-device-type": "web"
        }
        with requests.Session() as session:
            # Send post request to login to get two factor authentication token
            login_url = f"{self.BASE_URL}{ApiEndpoint.LOGIN}"
            payload = {
                "login_id": Config.USERNAME,
                "password": Config.PASSWORD,
                "device": "WEB"
            }
            response = session.post(url=login_url, data=json.dumps(payload), headers=headers)
            if not response.ok:
                self._logger.error(f"Non 200 status code from {login_url}")
                self._logger.error(response.text)
                raise AliceBlueApiError("Non 200 status code")
            # Send post request for two FA authentication
            data = response.json()["data"]
            twofa_data = data["twofa"]
            twofa_token = twofa_data["twofa_token"]
            twofa_type = twofa_data["type"]
            twofa_questions = twofa_data["questions"]
            twofa_url = f"{self.BASE_URL}{ApiEndpoint.TWO_FA}"
            payload = {
                "login_id": Config.USERNAME,
                "twofa": [
                    {"question_id": str(x["question_id"]), "answer": Config.TWO_FA_ANSWER}
                    for x in twofa_questions
                ],
                "twofa_token": twofa_token,
                "type": twofa_type
            }
            response = session.post(url=twofa_url, data=json.dumps(payload), headers=headers)
            if not response.ok:
                self._logger.error(f"Non 200 status code from {twofa_url}")
                self._logger.error(response.text)
                raise AliceBlueApiError("Non 200 status code")
            data = response.json()["data"]
            return data["auth_token"]

    def generate_access_token(self):
        """ Get access token """
        session = requests.Session()
        url = f"{self.BASE_URL}{ApiEndpoint.AUTHORIZE}?response_type=code&" \
              f"state=test_state&client_id={Config.APPID}&redirect_uri={Config.REDIRECT_URL}"
        response = session.get(url)
        if "OAuth 2.0 Error" in response.text:
            self._logger.error(
                "OAuth 2.0 Error occurred. Please verify your app id and redirect url"
            )
        soup = BeautifulSoup(response.text, features="html.parser")
        csrf_token = soup.find("input", attrs={"name": "_csrf_token"})["value"]
        login_challenge = soup.find("input", attrs={"name": "login_challenge"})["value"]
        payload = {
            "client_id": Config.USERNAME,
            "password": Config.PASSWORD,
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
            "answer1": Config.TWO_FA_ANSWER,
            "answer2": Config.TWO_FA_ANSWER,
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
        # Get Access Token
        payload = {
            "code": code,
            "redirect_uri": Config.REDIRECT_URL,
            "grant_type": "authorization_code"
        }
        url = f"{self.BASE_URL}{ApiEndpoint.ACCESS_TOKEN}"
        response = session.post(url, auth=(Config.APPID, Config.APPSECRET), data=payload)
        json_data = response.json()
        if "access_token" in json_data:
            access_token = json_data["access_token"]
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

    def nfo_setup(self):
        """ Get all the required master contracts """
        self._master_contracts_nfo = self.get_master_contracts(exchange=Exchanges.NFO.name)
        self._options_master_contracts = self._master_contracts_nfo["NSE-OPT"]
        self._future_master_contracts = self._master_contracts_nfo["NSE-FUT"]
        self.create_banknifty_instruments()
        
    def nse_setup(self):
        """ Get all the required master contracts for stock and indices """
        self._master_contracts_nse = self.get_master_contracts(exchange=Exchanges.NSE.name)
        self._nse_indices_contracts = self._master_contracts_nse["NSE-IND"]
        self._nse_stock_contracts = self._master_contracts_nse["NSE"]
        self.create_nifty_index()
        self.create_banknifty_index()
        self.create_indiavix_index()

    def get_master_contracts(self, exchange):
        """ Get all the tradable contracts of an exchange """
        return self.api_call(
            endpoint=ApiEndpoint.MASTER_CONTRACT,
            method="GET",
            query_params={"exchange": exchange}
        )

    def create_banknifty_instruments(self):
        """ Return list of bnf instruments from master contracts """
        self._bnf_instruments = [
            Instrument.create(x)
            for x in self._options_master_contracts if x["symbol"].startswith("BANKNIFTY")
        ]
        self._bnf_instruments += [
            Instrument.create(x)
            for x in self._future_master_contracts if x["symbol"].startswith("BANKNIFTY")
        ]

    def create_nifty_instruments(self):
        """ Return list of nifty instruments from master contracts """
        self._nifty_instruments = [
            Instrument.create(x)
            for x in self._options_master_contracts if x["symbol"].startswith("NIFTY")
        ]
        self._nifty_instruments += [
            Instrument.create(x)
            for x in self._future_master_contracts if x["symbol"].startswith("NIFTY")
        ]

    def create_nifty_index(self):
        """ Create nifty index NSEIndex """
        nifty_index = next(
            (x for x in self._nse_indices_contracts if x["symbol"] == "Nifty 50"),
            None
        )
        if nifty_index is not None:
            self._nifty_index = Instrument.create(nifty_index)

    def create_banknifty_index(self):
        """ Create banknifty index NSEIndex """
        banknifty_index = next(
            (x for x in self._nse_indices_contracts if x["symbol"] == "Nifty Bank"),
            None
        )
        if banknifty_index is not None:
            self._banknifty_index = Instrument.create(banknifty_index)

    def create_indiavix_index(self):
        """ Create india vix index NSEIndex """
        inida_vix_index = next(
            (x for x in self._nse_indices_contracts if x["symbol"] == "India VIX"),
            None
        )
        if inida_vix_index is not None:
            self._india_vix_index = Instrument.create(inida_vix_index)

    def get_banknifty_option_instrument(
            self, strike: int, expiry: datetime.date, option_type: OptionType
    ) -> Optional[Instrument]:
        """ Get Call Option instrument by strike and expiry for banknifty """
        return next(
            (
                x for x in self._bnf_instruments
                if x.option_type == option_type and x.strike == strike and x.expiry == expiry
            ),
            None
        )

    def get_banknifty_future_instrument(self, expiry: datetime.date):
        """ Get future instrument for banknifty """
        return next(
            (
                x for x in self._bnf_instruments
                if x.option_type == OptionType.FUT and x.expiry == expiry
            ),
            None
        )

    def get_nifty_option_instrument(
            self, strike: int, expiry: datetime.date, option_type: OptionType
    ) -> Optional[Instrument]:
        """ Get Call Option instrument by strike and expiry for nifty"""
        return next(
            (
                x for x in self._nifty_instruments
                if x.option_type == option_type and x.strike == strike and x.expiry == expiry
            ),
            None
        )

    def get_nifty_future_instrument(self, expiry: datetime.date):
        """ Get future instrument for nifty """
        return next(
            (
                x for x in self._nifty_instruments
                if x.option_type == OptionType.FUT and x.expiry == expiry
            ),
            None
        )

    @property
    def banknifty_instruments(self) -> List[Instrument]:
        return self._bnf_instruments

    @property
    def nifty_instruments(self) -> List[Instrument]:
        return self._nifty_instruments

    @property
    def access_token(self) -> str:
        if not self._access_token:
            self.refresh_access_token()
        return self._access_token

    @property
    def auth_token(self) -> str:
        if not self._auth_token:
            self.refresh_auth_token()
        return self._auth_token

    @property
    def nifty_index(self) -> Instrument:
        return self._nifty_index

    @property
    def banknifty_index(self) -> Instrument:
        return self._banknifty_index

    @property
    def india_vix_index(self) -> Instrument:
        return self._india_vix_index
