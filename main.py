"""
File:           main.py
Author:         Dibyaranjan Sathua
Created on:     20/03/21, 1:40 pm
"""
import time
import json
import logging
from kiteconnect import KiteConnect, KiteTicker

logging.basicConfig(level=logging.DEBUG)


kite = KiteConnect(api_key="7o631u0sjrn9bsuu")
# Login url
# https://kite.trade/connect/login?api_key=7o631u0sjrn9bsuu&v=3
# print(kite.login_url())
data = kite.generate_session("L4LW7bQH4A9TyHcCdrTD16TxSpcQlztA", api_secret="9livcjl9wu8qm2ape59ci2tzm5713wac")
kite.set_access_token(data["access_token"])
kite_ticker = KiteTicker("7o631u0sjrn9bsuu", data["access_token"])

# Initialise
kws = KiteTicker("7o631u0sjrn9bsuu", data["access_token"])

counter = 1

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    global counter
    filenme = f"/Users/dibyaranjan/Stocks/stocklabs/data/data{counter}.json"
    with open(filenme, mode="w") as fh_:
        json.dump(ticks, fh_, indent=4, sort_keys=True, default=str)
    # logging.debug("Ticks: {}".format(ticks))
    last_traded_time = ticks[0]['last_trade_time']
    timestamp = ticks[0]['timestamp']
    logging.debug(f"Last price for 14800 CE {ticks[0]['last_price']}")
    logging.debug(f"Last traded time: {last_traded_time}")
    logging.debug(f"timestamp: {timestamp}")
    logging.debug(f"Dumping data to {filenme}")
    counter += 1
    # time.sleep(60)


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([11220226, 11223810])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [11220226, 11223810])


def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()


# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
