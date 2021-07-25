"""
File:           base_trading_system.py
Author:         Dibyaranjan Sathua
Created on:     21/03/21, 10:44 pm
"""
from abc import ABC, abstractmethod


class BaseTradingSystem(ABC):
    """ Contains common functions used by Trading Systems """
    @abstractmethod
    def execute(self):
        """ Should be implemented in the child class """
        pass

