"""
File:           bnf_intraday_straddle.py
Author:         Dibyaranjan Sathua
Created on:     11/07/21, 4:49 pm
"""
from typing import Optional
import datetime
import time
from trading_systems.base_trading_system import BaseTradingSystem
from alice_blue_api.candle import CandleApi, CandleTimeFrame, InstrumentCandle
from trading_systems.exceptions import TradingSystemError
from utils.strike_selection import StrikeSelection


class BNFIntradayStraddle(BaseTradingSystem):
    """
    Intraday straddle on BNF. (https://www.youtube.com/watch?v=LlQUdobJWFQ&t=1078s)
    Entry condition (optional): Check if open price is within previous day range, take the trade.
    Secondary condition: Previous day high and low are not broken in next 15 mins till 9:30AM
    Trade start time: 9:30 AM
    Create straddle at ATM strike.
    SL: Trailing
    """
    ALICE_BLUE_BNF_INDEX_TOKEN: int = 26009       # bnf index token

    def __init__(self):
        super(BNFIntradayStraddle, self).__init__()
        self._candle_api_index: CandleApi = CandleApi.for_nse_indices()
        self._candle_api_nfo: CandleApi = CandleApi.for_nfo()
        self._prev_day_high: Optional[float] = None
        self._prev_day_low: Optional[float] = None
        self._entry_candle: Optional[InstrumentCandle] = None
        self._straddle_strike: Optional[int] = None
        self._entry_time: datetime.time = datetime.time(hour=9, minute=36)

    def check_entry_condition(self) -> bool:
        """ Check if entry condition is True """
        today_open_price = self._candle_api_index.get_todays_open_price()
        if self._prev_day_low <= today_open_price <= self._prev_day_high:
            return True
        return False

    def check_secondary_entry_condition(self) -> bool:
        """ Check if previous day high and low are broken till entry time """
        if self._prev_day_low <= self._entry_candle.close <= self._prev_day_high:
            return True
        return False

    def _get_bnf_index_candles(self):
        """ Get bnf candles data """
        to_date = datetime.datetime.now()
        five_days = datetime.timedelta(days=5)
        from_date = to_date - five_days
        # Getting 5 min candle data for last 5 days
        self._candle_api_index.send_request(
            instrument_token=self.ALICE_BLUE_BNF_INDEX_TOKEN,
            timeframe=CandleTimeFrame.FIVE_MINUTE,
            to_date=to_date,
            from_date=from_date
        )
        if not self._candle_api_index.request_successful:
            raise TradingSystemError(f"Non 200 status code from kite candle API")

    def execute(self):
        """ execute the trade """
        # Get bnf candles data
        self._get_bnf_index_candles()
        # Get previous day high low
        self._prev_day_high, self._prev_day_low = \
            self._candle_api_index.get_previous_trading_day_high_low()
        if self._prev_day_high is None or self._prev_day_low is None:
            raise TradingSystemError(f"Error fetching previous trading day high and low")
        # Get the 9:30 AM candle
        self._entry_candle = self._candle_api_index.get_todays_price_by_time(
            time=self._entry_time
        )
        if self._entry_candle is None:
            raise TradingSystemError(f"Error fetching {self._entry_time} candle data")
        self._straddle_strike = StrikeSelection.get_nearest_100_strike(self._entry_candle.close)

    def wait_till_entry(self):
        """ Wait till 9:35 AM to take an entry """
        while True:
            now = datetime.datetime.now().time()
            if now.hour == self._entry_time.hour and now.min >= self._entry_time.minute:
                break
            time.sleep(60)

    @property
    def entry_time(self) -> datetime.time:
        return self._entry_time

    @entry_time.setter
    def entry_time(self, time: datetime.time):
        self._entry_time = time
