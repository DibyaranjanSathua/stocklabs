"""
File:           alice_blue.py
Author:         Dibyaranjan Sathua
Created on:     21/06/21, 11:20 am
"""
import datetime
import time
from alice_blue_api.api import AliceBlueApi
from alice_blue_api.enums import OptionType, FeedModes, FeedAction
from alice_blue_api.websocket import AliceBlueWebSocket


def main():
    """ Main testing function """
    obj = AliceBlueApi.get_handler()
    obj.api_setup()
    obj.nfo_setup()
    obj.nse_setup()
    print(obj.access_token)
    print(obj.auth_token)
    instrument_ce = obj.get_banknifty_option_instrument(
        strike=36000, expiry=datetime.date(2021, 8, 26), option_type=OptionType.CE
    )
    instrument_pe = obj.get_banknifty_option_instrument(
        strike=36000, expiry=datetime.date(2021, 8, 26), option_type=OptionType.PE
    )
    instrument_fut = obj.get_banknifty_future_instrument(expiry=datetime.date(2021, 8, 26))
    print(instrument_ce.code)
    print(instrument_pe.code)
    print(instrument_fut.code)
    data = {
        "a": FeedAction.SUBSCRIBE.value,
        "v": [
            (instrument_ce.exchange_code, instrument_ce.code),
            (instrument_pe.exchange_code, instrument_pe.code),
            (instrument_fut.exchange_code, instrument_fut.code),
            (obj.nifty_index.exchange_code, obj.nifty_index.code),
            (obj.banknifty_index.exchange_code, obj.banknifty_index.code),
            (obj.india_vix_index.exchange_code, obj.india_vix_index.code)
        ],
        "m": FeedModes.COMPACT_MARKETDATA.value
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
