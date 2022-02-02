"""
File:           base_trading_system.py
Author:         Dibyaranjan Sathua
Created on:     21/03/21, 10:44 pm
"""
from typing import Optional
from abc import ABC, abstractmethod

from alice_blue_api.api import AliceBlueApi
from alice_blue_api.option_chain import OptionChain
from utils.expiry_selection import Expiry
from google_sheet_api import SheetReader, SheetWriter


class BaseTradingSystem(ABC):
    """ Contains common functions used by Trading Systems """

    def __init__(self):
        token_file = "/Users/dibyaranjan/Stocks/stocklabs/google_token/token.json"
        self._paper_trade: bool = False
        self._expiry: Optional[Expiry] = None
        self._alice_blue_api_handler: AliceBlueApi = AliceBlueApi.get_handler()
        self._option_chain: OptionChain = OptionChain.get_instance()
        self._sheet_reader: SheetReader = SheetReader(token_file=token_file)
        self._sheet_writer: SheetWriter = SheetWriter(token_file=token_file)

    @property
    def paper_trade(self) -> bool:
        return self._paper_trade

    @paper_trade.setter
    def paper_trade(self, value):
        self._paper_trade = value

    @property
    def expiry(self) -> Optional[Expiry]:
        return self._expiry

    @expiry.setter
    def expiry(self, value: Expiry):
        self._expiry = value

    @abstractmethod
    def execute(self):
        """ Should be implemented in the child class """
        pass

