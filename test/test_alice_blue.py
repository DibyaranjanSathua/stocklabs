"""
File:           alice_blue.py
Author:         Dibyaranjan Sathua
Created on:     21/06/21, 11:20 am
"""
import datetime
import time
from alice_blue_api.api import AliceBlueApi
from alice_blue_api.enums import OptionType
from alice_blue_api.websocket import AliceBlueWebSocket
from alice_blue_api.websocket_streams import MarketData, CompactMarketData


def test_websocket_streams():
    """ Testing websocket streams """
    # binary_data = b'\x01\x02\x00\x00\xab\xa6\x00\x00e\t`\xd0+[\x00\x00\x00\x19\x00\x06V]\x00' \
    #               b'\x00d\xcd\x00\x00\x00K\x00\x00e;\x00\x00\x00d\x00\x00\x00\x00\x00\x00\\\xc6' \
    #               b'\x00\x00\x00\x00\x00\x00\\\xad\x00\x00`X`\xd0+d\x00\x00Y.\x00\x00rB\x00' \
    #               b'\x00B\x81\x00\x00\x96s\x00\x00rB\x00\x00\x00\x00\x00\x00\x00\x05\x00\x02' \
    #               b'\xec\xfc\x00\x02\x12F\x00\x01qV'

    binary_data = b'\x01\x02\x00\x00\xab\xa6\x00\x00e\t`\xd0+[\x00\x00\x00\x19\x00\x06V]\x00' \
                  b'\x00e\x13\x00\x00\x00K\x00\x00er\x00\x00\x00\x19\x00\x00\x00\x00\x00' \
                  b'\x00]\\\x00\x00\x00\x00\x00\x00\\0\x00\x00`X`\xd0+g\x00\x00Y.\x00\x00rB' \
                  b'\x00\x00B\x81\x00\x00\x96s\x00\x00rB\x00\x00\x00\x00'
    binary_data = b'\x01\x02\x00\x00\xcc\x12\x00\x00\xb0,`\xd4W\x9e\x00\x00\x00\x19\x00\x19x' \
                  b'\xb4\x00\x00\xb0"\x00\x00\x002\x00\x00\xb7\x98\x00\x00\x002\x00\x00\x00' \
                  b'\x00\x00\x00k!\x00\x00\x00\x00\x00\x00Rl\x00\x00\xafr`\xd4W\xa0\x00\x00\x95' \
                  b'\xce\x00\x00\xcf\x03\x00\x00\x8a \x00\x00\x94f\x00\x00\xcf\x03\x00\x00\x00\x00'
    binary_data = b"\x01\x02\x00\x00\xcc\x13\x00\x00\x83\x8b`\xd4W\x9f\x00\x00\x00\xaf\x00\x15" \
                  b"\x0f6\x00\x00\x7f\xbc\x00\x00\x00\xc8\x00\x00\x83\x8b\x00\x00\x00\x19\x00" \
                  b"\x00\x00\x00\x00\x00h\xfb\x00\x00\x00\x00\x00\x00xP\x00\x00\x91P`\xd4W" \
                  b"\xa0\x00\x00\xc9@\x00\x00\xd3'\x00\x00}\x00\x00\x00\xcag\x00\x00\xd3'\x00\
                  x00\x00\x00"
    data = MarketData.create(binary_data)
    print(data.token)
    print(data.ltp)
    print(data.open)
    print(data.close)
    print(data.high)
    print(data.low)
    print(data.last_trade_time)
    print(data.exchange_timestamp)


def test_websocket_compact_market():
    binary_data = b'\x02\x02\x00\x00\xcc\x12\x00\x00\xb0,\x00\x00\x1b\xc6`\xd4W\x9e\x00\x00\x00' \
                  b'\x05\x00\x03\x0by\x00\x02\xba\x89\x00\x01\xbfD\x00\x00\xb0"\x00\x00\xb7\x98'
    # binary_data = b'\x02\x02\x00\x00\xcc\x13\x00\x00\x83\x8b\xff\xff\xb9$`\xd4W\x9f\x00\x00\x00' \
    #               b'\x05\x00\x03\x90X\x00\x02\x98t\x00\x00\x81L\x00\x00\x7f\xbc\x00\x00\x83\x8b'
    binary_data = b'\x02\x02\x00\x00\xcf\xbb\x005v\xd6\x00\x00v\xe3`\xd4W\x9f\x000\x117\x00:\xbf' \
                  b'\xb0\x00\x1c\xdf\xe5\x00\x11\xaf\xa3\x005t`\x005w\x1c'
    data = CompactMarketData.create(binary_data)
    print(data.token)
    print(data.ltp)


def main():
    """ Main testing function """
    obj = AliceBlueApi.get_handler()
    obj.api_setup()
    obj.option_setup()
    print(obj.access_token)
    print(obj.auth_token)
    instrument_ce = obj.get_bnf_option_instrument(
        strike=34800, expiry=datetime.date(2021, 7, 29), option_type=OptionType.CE
    )
    instrument_pe = obj.get_bnf_option_instrument(
        strike=34800, expiry=datetime.date(2021, 7, 29), option_type=OptionType.PE
    )
    instrument_fut = obj.get_bnf_future_instrument(expiry=datetime.date(2021, 7, 29))
    print(instrument_ce.code)
    print(instrument_pe.code)
    print(instrument_fut.code)
    data = {
        "a": "subscribe",
        "v": [
            (instrument_ce.exchange_code, instrument_ce.code),
            (instrument_pe.exchange_code, instrument_pe.code),
            (instrument_fut.exchange_code, instrument_fut.code),
        ],
        "m": "compact_marketdata"
    }
    print(data)
    ws = AliceBlueWebSocket()
    ws.start(thread=True)
    ws.send_heartbeat()
    ws.wait_until_connection_open()
    print("reach this point")
    ws.send(data)
    time.sleep(60)


if __name__ == "__main__":
    main()
    # test_websocket_streams()
    # test_websocket_compact_market()
