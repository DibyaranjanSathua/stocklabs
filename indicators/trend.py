"""
File:           trend.py
Author:         Dibyaranjan Sathua
Created on:     20/03/21, 11:23 am
"""
from typing import Tuple, List
from indicators.base_indicator import BaseIndicator


class VWAPIndicator(BaseIndicator):
    """
    VWAP (Volume Weighted Average Price) = Summation (Price * Volume) / Sumation of Volume
    Price = (High + Low + Close) / 3
    https://www.investopedia.com/terms/v/vwap.asp
    """
    def __init__(
            self,
            high: float,
            low: float,
            close: float,
            volume: float,
            prev_sum_pv: float = 0,
            prev_sum_v: float = 0
    ):
        """
        Constructor.
        Args:
            high: Current period price high
            low: Current period price low
            close: Current period price close
            volume: Current period volume
            prev_sum_pv: Previous summation of P * V. For first candle it will be zero.
            prev_sum_v: Previous summation of V. For first candle it will be zero.
        """
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume
        self._prev_sum_pv = prev_sum_pv
        self._prev_sum_v = prev_sum_v

    def calc(self) -> Tuple[float, float, float]:
        """ Calculate the VWAP """
        price = (self._high + self._low + self._close) / 3
        sum_pv = price * self._volume + self._prev_sum_pv
        sum_v = self._volume + self._prev_sum_v
        return round(sum_pv/sum_v, 2), sum_pv, sum_v


class SMAIndicator(BaseIndicator):
    """ Simple moving average """

    def __init__(self, data: List[float], period: int):
        self._data = data
        self._period = period

    def calc(self) -> float:
        """ Calculate """
        return self.sma(src=self._data, period=self._period)
