"""
File:           momentum.py
Author:         Dibyaranjan Sathua
Created on:     20/03/21, 11:54 am
"""
from typing import List, Optional, Tuple
from indicators.base_indicator import BaseIndicator
from indicators.exceptions import IndicatorException


class RSIIndicator(BaseIndicator):
    """
    RSI (Relative Strength Index)
    We will be using Exponentially weighted moving average with alpha = 1 / period.
    RS = Average Gain over N period / Average Loss over N period
    Gain means previous day close < current day close
    Loss means previous day close > current day close
    RSI = 100 - (100/1+RS)
    https://www.investopedia.com/terms/r/rsi.asp
    """
    def __init__(
            self,
            close: List[float],
            period: Optional[int] = None,
            prev_avg_gain: Optional[float] = None,
            prev_avg_loss: Optional[float] = None,
            initial: bool = False
    ):
        """
        Constructor.
        Args:
            close: List of previous close price or new candle close value. Latest close value will
            be in the beginning and older ones are towards the end.
            period: No of period to calculate the RSI.
            If None, it will take number of elements in prev_close.
            prev_avg_gain: Use to calculate the next RSI value.
            prev_avg_loss: Use to calculate the next RSI value.
            initial: Indicate if RSI calculation is done on some initial candles or
            for the current candle
        """
        self._close = close
        self._period = period if period is not None else len(close)
        self._prev_avg_gain = prev_avg_gain
        self._prev_avg_loss = prev_avg_loss
        self._initial = initial
        # For a period of N we need N+1 close price. Because the first one acts as dummy and
        # has no change
        if self._initial:
            if len(close) + 1 < self._period:
                raise IndicatorException(
                    f"Period {self._period} can't be more than number of elements in close plus 1"
                )
        else:
            # RSI for current candle
            if prev_avg_gain is None or prev_avg_loss is None:
                raise IndicatorException(
                    f"prev_avg_gain and prev_avg_loss must be provided for calculating RSI "
                    f"for a new candle (single close value instead of list)"
                )
            if len(self._close) < 2:
                raise IndicatorException(
                    f"For current candle RSI, close arguments should have 2 elements"
                )

    def calc(self) -> Tuple[float, float, float]:
        """ Calculate the RSI """
        # Remember that prices will have lastest close price in the beginning and older ones
        # towards the end
        gain = []
        loss = []
        if self._initial:
            prices = self._close[:self._period + 1]
            for i in range(len(prices) - 1):
                change = prices[i] - prices[i+1]
                if change > 0:
                    gain.insert(0, change)
                    loss.insert(0, 0)
                else:
                    gain.insert(0, 0)
                    loss.insert(0, abs(change))

        else:
            # For current candle we last candle close price and current candle close price
            prices = self._close[:2]
            change = prices[0] - prices[1]
            gain = 0 if change < 0 else change
            loss = 0 if change > 0 else abs(change)
        # print(gain)
        # print(loss)
        avg_gain = self.rma(src=gain, period=self._period, average=self._prev_avg_gain)
        avg_loss = self.rma(src=loss, period=self._period, average=self._prev_avg_loss)
        if avg_loss == 0:
            return 100, avg_gain, avg_loss
        elif avg_gain == 0:
            return 0, avg_gain, avg_loss
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100/(1+rs))
            return round(rsi, 2), avg_gain, avg_loss
