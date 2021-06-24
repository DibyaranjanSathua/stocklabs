"""
File:           options_smart_buy.py
Author:         Dibyaranjan Sathua
Created on:     21/03/21, 10:47 pm
"""
from indicators.trend import VWAPIndicator, SMAIndicator
from indicators.momentum import RSIIndicator
from trading_systems.base_trading_system import BaseTradingSystem


class OptionsSmartBuy(BaseTradingSystem):
    """
    Strategy to buy CE or PE options for nifty or banknifty depending on the following conditions.
    1. Price > VWAP
    2. Volume > 20 SMA of Volume
    3. RSI > 60
    4. OI < 20 SMA of OI (OI unwinding)
    """
    def __init__(self):
        pass

    def signal_vwap(self):
        """ Signal for price > vwap """
        pass

    def signal_volume(self):
        """ Signal for volume > 20 SMA """
        pass

    def signal_rsi(self):
        """ Signal for RSI > 60 """
        pass

    def signal_oi(self):
        """ Signal for OI < 20 SMA """
        pass

