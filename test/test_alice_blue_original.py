"""
File:           test_alice_blue_priginal.py
Author:         Dibyaranjan Sathua
Created on:     25/06/21, 10:37 am
"""
import datetime
import time
from alice_blue import *
from alice_blue_api.api import AliceBlueApi

obj = AliceBlueApi()
obj.api_setup()

# access_token = AliceBlue.login_and_get_access_token(
#     username='187812',
#     password='StockLabs123',
#     twoFA='STOCKLABS',
#     api_secret='I37wEAsdK9xxOx7BuqhHB2hQKoADtxWeteOsLwxxp4bq8JH4gOVA9PUW1gOzgA8m'
# )

alice = AliceBlue(
    username='187812',
    password='StockLabs123',
    access_token=obj.access_token,
    master_contracts_to_download=['NFO']
)

bn_call = alice.get_instrument_for_fno(
    symbol='BANKNIFTY',
    expiry_date=datetime.date(2021, 7, 1),
    is_fut=False,
    strike=34800,
    is_CE=True
)
print(bn_call.token)
socket_opened = False


def event_handler_quote_update(message):
    print(f"quote update {message}")


def open_callback():
    global socket_opened
    socket_opened = True


alice.start_websocket(subscribe_callback=event_handler_quote_update,
                      socket_open_callback=open_callback,
                      run_in_background=True)


while(socket_opened==False):
    pass


alice.subscribe(bn_call, LiveFeedType.COMPACT)
time.sleep(10)
