"""
File:           historical_price.py
Author:         Dibyaranjan Sathua
Created on:     06/07/21, 12:44 am
"""
from typing import Optional, List, Dict, Tuple
import datetime
from dataclasses import dataclass
import requests
import enum
from kite_api.config import Config


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


class CandleTimeFrame(enum.Enum):
    """ Candle timeframe """
    ONE_MINUTE = "minute"
    FIVE_MINUTE = "5minute"
    FIFTEEN_MINUTE = "15minute"
    THIRTY_MINUTE = "30minute"
    ONE_HOUR = "60minute"
    ONE_DAY = "day"


class KiteCandle:
    """ Kite internal API to get candle data of an instruments """
    BASE_URL = "https://kite.zerodha.com/oms/instruments/historical/{instrument_token}/" \
               "{timeframe}?user_id=TW1320&oi={oi}&from={from_date}&to={to_date}"

    def __init__(self):
        self._candles: List[InstrumentCandle] = []
        self._request_successful: bool = False
        self._today: Optional[datetime.date] = None

    def send_request(
            self,
            instrument_token: int,
            timeframe: CandleTimeFrame,
            from_date: datetime.date,
            to_date: datetime.date,
            open_interest: bool = True
    ):
        """ Send API request and create InstrumentCandle """
        from_date_str = from_date.strftime("%Y-%m-%d")
        to_date_str = to_date.strftime("%Y-%m-%d")
        oi = 1 if open_interest else 0
        url = KiteCandle.BASE_URL.format(
            instrument_token=instrument_token,
            timeframe=timeframe.value,
            from_date=from_date_str,
            to_date=to_date_str,
            oi=oi
        )
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "authorization": f"enctoken {Config.CANDLE_API_TOKEN}",
            "referer": "https://kite.zerodha.com/static/build/chart.html?v=2.9.2",
            "accept-language": "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5",
        }
        with requests.Session() as session:
            response = session.get(url=url, headers=headers)
            if response.ok:
                self._request_successful = True
                self._candles = self._get_candles(response.json())
            else:
                print("Error fetching data using Kite internal API.")

    def get_todays_open_price(self) -> float:
        """ Return today's open price """
        return self.get_todays_price_by_time(time=datetime.time(hour=9, minute=15)).open

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
