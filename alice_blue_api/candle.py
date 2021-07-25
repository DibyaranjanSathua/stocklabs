"""
File:           candle.py
Author:         Dibyaranjan Sathua
Created on:     24/07/21, 8:04 pm
"""
from typing import Optional, List, Dict, Tuple
import datetime
from dataclasses import dataclass
import requests
import brotli
import json
import enum
from alice_blue_api.api import AliceBlueApi


@dataclass()
class InstrumentCandle:
    """ Historical instrument prices """
    date: datetime.date
    time: datetime.time
    open: float
    high: float
    low: float
    close: float
    volume: float
    open_interest: Optional[float]

    @classmethod
    def create(cls, data: List):
        """ create object of this dataclass """
        timestamp = datetime.datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S%z")
        return cls(
            date=timestamp.date(),
            time=timestamp.time(),
            open=data[1],
            high=data[2],
            low=data[3],
            close=data[4],
            volume=data[5],
            open_interest=data[6] if len(data) == 7 else None
        )


class CandleTimeFrame(enum.IntEnum):
    """ Candle timeframe """
    ONE_MINUTE = 1
    FIVE_MINUTE = 2
    FIFTEEN_MINUTE = 3
    THIRTY_MINUTE = 4
    ONE_HOUR = 5
    FOUR_HOUR = 6
    ONE_DAY = 7


class CandleExchange(enum.Enum):
    """ Candle exchange """
    NSE = "NSE"                     # For stocks
    NSE_INDICES = "NSE_INDICES"     # For indices
    NFO = "NFO"                     # For Fut and Options


class CandleApi:
    """ Alice blue internal API to get candle data of an instrument """
    BASE_URL: str = "https://ant.aliceblueonline.com/api/v1/charts/tdv"

    @classmethod
    def for_nse_indicies(cls):
        """ API for nse indicies instruments """
        return cls(exchange=CandleExchange.NSE_INDICES)

    @classmethod
    def for_nfo(cls):
        """ APT for nfo instruments """
        return cls(exchange=CandleExchange.NFO)

    @classmethod
    def for_nse(cls):
        """ API for nse stocks instruments """
        return cls(exchange=CandleExchange.NSE)

    def __init__(self, exchange: CandleExchange):
        self._exchange: CandleExchange = exchange
        self._candles: List[InstrumentCandle] = []
        self._request_successful: bool = False
        self._today: Optional[datetime.date] = None
        self._alice_blue_api_handler: AliceBlueApi = AliceBlueApi.get_handler()

    def send_request(
            self,
            instrument_token: int,
            timeframe: CandleTimeFrame,
            from_date: datetime.datetime,
            to_date: datetime.datetime,
            open_interest: bool = False     # For future use
    ):
        """ Send API request and create InstrumentCandle """
        headers = self.get_headers()
        params = self.get_query_params(
            instrument_token=instrument_token,
            timeframe=timeframe,
            from_date=from_date,
            to_date=to_date
        )
        with requests.Session() as session:
            response = session.get(url=self.BASE_URL, params=params, headers=headers)
        if response.ok:
            self._request_successful = True
            # Check the content encoding
            # content_encoding = response.headers.get("Content-Encoding", "")
            # if content_encoding == "br":
            #     response_data = json.loads(brotli.decompress(response.content))
            #     self._candles = self._get_candles(response_data)
            # else:
            #     print(
            #         f"Content-Encoding is {content_encoding}. "
            #         f"Currenly only br encoding is supported."
            #     )
            self._candles = self._get_candles(response.json())
        else:
            print("Error fetching data using AliceBlue internal API.")

    def get_todays_open_price(self) -> Optional[float]:
        """ Return today's open price """
        nine_fifteen_candle = self.get_todays_price_by_time(time=datetime.time(hour=9, minute=15))
        if nine_fifteen_candle is not None:
            return nine_fifteen_candle.open

    def get_todays_price_by_time(self, time: datetime.time) -> InstrumentCandle:
        """ Return today's price by time """
        today = self._today if self._today is not None else datetime.date.today()
        candle = next((x for x in self._candles if x.date == today and x.time == time), None)
        if candle is not None:
            return candle
        print(f"No candle data for date {today} and time {time}")

    def get_previous_trading_day_high_low(self) -> Tuple[Optional[float], Optional[float]]:
        """ Return previous trading day's high low """
        today = self._today if self._today is not None else datetime.date.today()
        # Previous day can be a non-trading day. So check up to today - 5
        for day in range(1, 6):
            time_delta = datetime.timedelta(days=day)
            previous_day = today - time_delta
            candles = [x for x in self._candles if x.date == previous_day]
            if candles:
                break
        else:
            # Executed if for loop is not terminated by break statement
            print("No candles data found for the last 5 days")
            return None, None
        high = max(x.high for x in candles)
        low = min(x.low for x in candles)
        return high, low

    def get_query_params(
            self,
            instrument_token: int,
            timeframe: CandleTimeFrame,
            from_date: datetime.datetime,
            to_date: datetime.datetime
    ):
        """ Get query params """
        params = {
            "exchange": self._exchange.value,
            "token": instrument_token,
            "starttime": int(from_date.timestamp()),
            "endtime": int(to_date.timestamp())
        }
        if timeframe in [CandleTimeFrame.ONE_MINUTE, CandleTimeFrame.FIVE_MINUTE, CandleTimeFrame.FIFTEEN_MINUTE, CandleTimeFrame.THIRTY_MINUTE]:
            params["candletype"] = 1
            if timeframe == CandleTimeFrame.ONE_MINUTE:
                params["data_duration"] = 1
            elif timeframe == CandleTimeFrame.FIVE_MINUTE:
                params["data_duration"] = 5
            elif timeframe == CandleTimeFrame.FIFTEEN_MINUTE:
                params["data_duration"] = 15
            elif timeframe == CandleTimeFrame.THIRTY_MINUTE:
                params["data_duration"] = 30
        elif timeframe in [CandleTimeFrame.ONE_HOUR, CandleTimeFrame.FOUR_HOUR]:
            params["candletype"] = 2
            if timeframe == CandleTimeFrame.ONE_HOUR:
                params["data_duration"] = 1
            elif timeframe == CandleTimeFrame.FOUR_HOUR:
                params["data_duration"] = 4
        elif timeframe in [CandleTimeFrame.ONE_DAY]:
            params["candletype"] = 3
            if timeframe == CandleTimeFrame.ONE_DAY:
                params["data_duration"] = 1
        return params

    def get_headers(self):
        """ Headers for the API request """
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "x-authorization-token": f"{self._alice_blue_api_handler.auth_token}",
            "referer": "https://ant.aliceblueonline.com/mobilecharts/",
            "accept-language": "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br"
        }
        return headers

    @staticmethod
    def _get_candles(json_data: Dict):
        """ Convert json data into list on InstrumentCandles """
        candles = json_data["data"]["candles"]
        return [InstrumentCandle.create(x) for x in candles]

    @property
    def candles(self) -> List[InstrumentCandle]:
        return self._candles

    @property
    def request_successful(self) -> bool:
        return self._request_successful

    @property
    def today(self) -> datetime.date:
        return self._today

    @today.setter
    def today(self, today: datetime.date):
        self._today = today
