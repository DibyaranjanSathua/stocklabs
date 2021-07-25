"""
File:           instruments.py
Author:         Dibyaranjan Sathua
Created on:     12/06/21, 12:44 pm
"""
from typing import Optional
from dataclasses import dataclass
import datetime

from alice_blue_api.enums import OptionType


@dataclass()
class Instrument:
    trading_symbol: str
    symbol: str
    lot_size: Optional[int]
    expiry: Optional[datetime.date]
    exchange_code: Optional[int]
    exchange: str
    code: int
    option_type: Optional[OptionType]
    strike: Optional[int]

    @classmethod
    def create(cls, data):
        """ Create Instrument class object from the input data """
        lot_size = None
        expiry = None
        option_type = None
        strike = None
        if "lotSize" in data:
            lot_size = int(data["lotSize"])
        if "expiry" in data:
            expiry = datetime.datetime.fromtimestamp(data["expiry"]).date()
        code = int(data["code"])
        # Check if the data is for Index Instrument
        symbol_parts = data["symbol"].split(" ")
        if symbol_parts[-1] == "CE":
            option_type = OptionType.CE
            # strike will be in float. S0 first convert it to float then int
            strike = int(float(symbol_parts[-2]))
        elif symbol_parts[-1] == "PE":
            option_type = OptionType.PE
            strike = int(float(symbol_parts[-2]))
        elif symbol_parts[-1] == "FUT":
            option_type = OptionType.FUT
            strike = None

        return cls(
            trading_symbol=data["trading_symbol"],
            symbol=data["symbol"],
            lot_size=lot_size,
            expiry=expiry,
            exchange_code=data["exchange_code"],
            exchange=data["exchange"],
            code=code,
            option_type=option_type,
            strike=strike
        )
