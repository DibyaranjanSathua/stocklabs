"""
File:           websocket.py
Author:         Dibyaranjan Sathua
Created on:     04/04/21, 4:55 pm
"""
from kiteconnect import KiteConnect, KiteTicker
from kite_api.config import Config


kite = KiteConnect(api_key=Config.API_KEY)
# Login url
# https://kite.trade/connect/login?api_key=<api_key>&v=3
# print(kite.login_url())
data = kite.generate_session(Config.REQUEST_TOKEN, api_secret=Config.API_SECRET)
kite.set_access_token(data["access_token"])
kite_ticker = KiteTicker(Config.API_KEY, data["access_token"])
instruments = kite.instruments('NFO')
# name should be "NIFTY" or "BANKNIFTY"
for contract in instruments:
    if "NIFTY" in contract['tradingsymbol']:
        token_detail = {'token': contract['instrument_token'], 'symbol': contract['tradingsymbol'], 'strike': contract['strike'],
                    'type': contract['instrument_type'], 'name': contract['name'], 'LTP': contract['last_price'],
                        'expiry': contract['expiry'], 'exchange': contract['exchange']
                    }
        if contract['instrument_token'] == 11220226:
            print(f"--> {contract['tradingsymbol']}")
        print(token_detail)
