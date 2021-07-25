"""
File:           option_chain.py
Author:         Dibyaranjan Sathua
Created on:     25/06/21, 2:05 pm
"""
from typing import Optional, Dict
from alice_blue_api.websocket_streams import MarketData
from alice_blue_api.instruments import Instrument


class OptionChain:
    """ Singleton class which stores option chain data """
    __instance: Optional["OptionChain"] = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(OptionChain, cls).__new__(cls, *args, **kwargs)
            return cls.__instance
        raise SyntaxError("This is a Singleton class. Use get_instance() method")

    def __init__(self):
        # Use for other variable initialization
        self.__option_chain: Dict = dict()

    @classmethod
    def get_instance(cls):
        """ Get or create instance """
        if cls.__instance is None:
            cls.__instance = OptionChain()
        return cls.__instance

    @classmethod
    def reset(cls):
        """ Method for test purposes. Don't use it in real code """
        cls.__instance = None

    def update(self, data: MarketData):
        """ Parse the binary data and add to Option Chain """
        self.__option_chain[data.token] = data

    def get_market_data_by_instrument(self, instrument: Instrument) -> MarketData:
        """ Get the market data by instrument """
        return self.__option_chain[instrument.code]
