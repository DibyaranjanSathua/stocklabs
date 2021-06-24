"""
File:           base_indicator.py
Author:         Dibyaranjan Sathua
Created on:     20/03/21, 11:24 am
"""
from typing import Optional, List, Union
from indicators.exceptions import IndicatorException


class BaseIndicator:
    """ Class containing some common functions """
    @staticmethod
    def sma(src: List[float], period: int) -> float:
        """ Simple moving average """
        if len(src) < period:
            raise IndicatorException(
                f"Period {period} can't be more than number of elements in src"
            )
        avg = sum(src[len(src) - period:]) / period
        return round(avg, 2)

    @staticmethod
    def rma(src: Union[List[float], float], period: int, average: Optional[float] = None) -> float:
        """
        Calculated the exponentially weighted moving average. Used is RSI.
        Args:
            src: For initial calculation it will be a list of values. For next candle, just pass
            a single value and the previous average.
            period: No of period
            average: Previous candle average

        Returns:

        """
        alpha = round(1/period, 2)
        if type(src) == list:
            # Initial calculation
            return BaseIndicator.sma(src=src, period=period)
        # Calculation for next candle
        if average is None:
            raise IndicatorException(
                f"Average must be provided for calculating rma from a single src value"
            )
        return alpha * src + (1 - alpha) * average
