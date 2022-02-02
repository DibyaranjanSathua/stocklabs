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


class FeedModes(enum.Enum):
    """ Different modes """
    MARKET_DATA = "marketdata"
    COMPACT_MARKETDATA = "compact_marketdata"
    SNAPQUOTE = "snapquote"
    FULL_SNAPQUOTE = "full_snapquote"
    SPREADDATA = "spreaddata"
    SPREAD_SNAPQUOTE = "spread_snapquote"
    DPR = "dpr"
    OI = "oi"
    MARKET_STATUS = "market_status"
    EXCHANGE_MESSAGES = "exchange_messages"


class FeedAction(enum.Enum):
    """ Action sent to web socket API """
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    HEARTBEAT = "h"
