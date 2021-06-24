"""
File:           constants.py
Author:         Dibyaranjan Sathua
Created on:     14/06/21, 12:49 am
"""
import enum


class OptionType(enum.Enum):
    """ Option Type, Call Option or Put Option """
    CE = 1
    PE = 2
    FUT = 3


class Exchanges(enum.Enum):
    """ Exchanges. Number represents their code (alice blue api documentation) """
    NSE = 1
    NFO = 2
    CDS = 3
    MCX = 4
    BSE = 6
    BFO = 7
