"""
File:           short_straddle.py
Author:         Dibyaranjan Sathua
Created on:     27/07/21, 1:41 am
"""
from typing import Optional
import datetime
from strategies.base_strategy import BaseStrategy
from alice_blue_api.instruments import Instrument


class ShortStraddle(BaseStrategy):
    """ Short Straddle strategy. Sell CE and PE same strike mostly ATM strike """

    def __init__(self, strike: int, expiry: datetime.date):
        super(ShortStraddle, self).__init__()
        self._strike: int = strike
        self._expiry: datetime.date = expiry
        self._pe_instrument: Optional[Instrument] = None
        self._ce_instrument: Optional[Instrument] = None


class ShortBankNiftyStraddle(ShortStraddle):
    """ Bank nifty short straddle """

    def __init__(self, strike: int, expiry: datetime.date):
        super(ShortBankNiftyStraddle, self).__init__(strike=strike, expiry=expiry)
