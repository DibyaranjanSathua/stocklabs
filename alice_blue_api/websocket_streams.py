"""
File:           websocket_streams.py
Author:         Dibyaranjan Sathua
Created on:     21/06/21, 7:15 pm
"""
from dataclasses import dataclass
import datetime
import struct

from alice_blue_api.enums import FeedModes


def unpack_int8(bin_data, pos):
    """ Convert 1 byte data """
    return struct.unpack(">B", bin_data[pos:pos+1])[0]


def unpack_int16(bin_data, pos):
    """ Convert 2 byte data """
    return struct.unpack(">H", bin_data[pos:pos+2])[0]


def unpack_int32(bin_data, pos):
    """ Convert 4 byte data """
    return struct.unpack(">I", bin_data[pos:pos+4])[0]


def unpack_int64(bin_data, pos):
    """ Convert 8 byte data """
    return struct.unpack(">Q", bin_data[pos:pos+8])[0]


def price_multiplier_by_exchange(exchange: int):
    """ Return a price multiplier function """
    if exchange in [1, 2, 4, 6, 7]:
        return lambda x: x / 100
    else:
        return lambda x: x / 10000000


def get_mode_from_stream(bin_data) -> FeedModes:
    """ Return the mode from the binary stream data (1st byte) """
    mode = unpack_int8(bin_data, 0)
    enum_mode = None
    if mode == 1:
        enum_mode = FeedModes.MARKET_DATA
    elif mode == 2:
        enum_mode = FeedModes.COMPACT_MARKETDATA
    elif mode == 3:
        enum_mode = FeedModes.SNAPQUOTE
    elif mode == 4:
        enum_mode = FeedModes.FULL_SNAPQUOTE
    elif mode == 5:
        enum_mode = FeedModes.SPREADDATA
    elif mode == 6:
        enum_mode = FeedModes.SPREAD_SNAPQUOTE
    elif mode == 7:
        enum_mode = FeedModes.DPR
    elif mode == 8:
        enum_mode = FeedModes.OI
    elif mode == 9:
        enum_mode = FeedModes.MARKET_STATUS
    elif mode == 10:
        enum_mode = FeedModes.EXCHANGE_MESSAGES
    return enum_mode


@dataclass()
class MarketData:
    """ Parse market binary data """
    exchange: int
    code: int
    ltp: int
    last_trade_time: datetime.datetime
    last_trade_quantity: int
    volume: int
    best_bid_price: int
    best_bid_quantity: int
    best_ask_price: int
    best_ask_quantity: int
    total_buy_quantity: int
    total_sell_quantity: int
    avg_trade_price: int
    exchange_timestamp: datetime.datetime
    open: int
    high: int
    low: int
    close: int
    yearly_high: int
    yearly_low: int

    @classmethod
    def create(cls, bin_data):
        """ Unpack the binary data and create MarketData object """
        # first byte will be ignored
        kwargs = dict()
        kwargs["exchange"] = unpack_int8(bin_data, 1)
        price_multiplier = price_multiplier_by_exchange(kwargs["exchange"])
        kwargs["code"] = unpack_int32(bin_data, 2)
        kwargs["ltp"] = price_multiplier(unpack_int32(bin_data, 6))
        kwargs["last_trade_time"] = datetime.datetime.fromtimestamp(unpack_int32(bin_data, 10))
        kwargs["last_trade_quantity"] = unpack_int32(bin_data, 14)
        kwargs["volume"] = unpack_int32(bin_data, 18)
        kwargs["best_bid_price"] = price_multiplier(unpack_int32(bin_data, 22))
        kwargs["best_bid_quantity"] = unpack_int32(bin_data, 26)
        kwargs["best_ask_price"] = price_multiplier(unpack_int32(bin_data, 30))
        kwargs["best_ask_quantity"] = unpack_int32(bin_data, 34)
        kwargs["total_buy_quantity"] = unpack_int64(bin_data, 38)
        kwargs["total_sell_quantity"] = unpack_int64(bin_data, 46)
        kwargs["avg_trade_price"] = price_multiplier(unpack_int32(bin_data, 54))
        kwargs["exchange_timestamp"] = datetime.datetime.fromtimestamp(unpack_int32(bin_data, 58))
        kwargs["open"] = price_multiplier(unpack_int32(bin_data, 62))
        kwargs["high"] = price_multiplier(unpack_int32(bin_data, 66))
        kwargs["low"] = price_multiplier(unpack_int32(bin_data, 70))
        kwargs["close"] = price_multiplier(unpack_int32(bin_data, 74))
        kwargs["yearly_high"] = price_multiplier(unpack_int32(bin_data, 78))
        kwargs["yearly_low"] = price_multiplier(unpack_int32(bin_data, 82))
        return cls(**kwargs)


@dataclass()
class CompactMarketData:
    """ Parse compact binary data """
    exchange: int
    code: int
    ltp: int
    change: int
    exchange_timestamp: datetime.datetime
    volume: int

    @classmethod
    def create(cls, bin_data):
        """ Unpack the binary data and create CompactData object """
        kwargs = dict()
        kwargs["exchange"] = unpack_int8(bin_data, 1)
        price_multiplier = price_multiplier_by_exchange(kwargs["exchange"])
        kwargs["code"] = unpack_int32(bin_data, 2)
        kwargs["ltp"] = price_multiplier(unpack_int32(bin_data, 6))
        kwargs["change"] = unpack_int32(bin_data, 10)
        kwargs["exchange_timestamp"] = datetime.datetime.fromtimestamp(unpack_int32(bin_data, 14))
        kwargs["volume"] = unpack_int32(bin_data, 18)
        return cls(**kwargs)
