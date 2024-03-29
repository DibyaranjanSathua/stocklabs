"""
File:           websocket.py
Author:         Dibyaranjan Sathua
Created on:     20/06/21, 7:36 pm

https://websocket-client.readthedocs.io/en/latest/app.html#websocket._app.WebSocketApp.__init__
"""
from typing import Optional
import json
import threading
import time
import websocket

from alice_blue_api.api import AliceBlueApi
from alice_blue_api.websocket_streams import MarketData, CompactMarketData, get_mode_from_stream
from alice_blue_api.option_chain import OptionChain
from alice_blue_api.enums import FeedModes, FeedAction


class AliceBlueWebSocket:
    """ Web socket connection to get live feed market data """
    WS_ENDPOINT: str = 'wss://ant.aliceblueonline.com/hydrasocket/v2/websocket' \
                       '?access_token={access_token}'

    def __init__(self):
        self._websocket: Optional[websocket.WebSocketApp] = None
        self._connected = False
        self._websocket_thread = None
        self._alice_blue_api_handler: AliceBlueApi = AliceBlueApi.get_handler()
        self._option_chain: OptionChain = OptionChain.get_instance()

    def connect(self):
        """ Connect to web socket """
        url = self.WS_ENDPOINT.format(access_token=self._alice_blue_api_handler.access_token)
        self._websocket = websocket.WebSocketApp(
            url=url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_message=self.on_message
        )

    def _run_forever(self):
        """ Run the websocket forever """
        while True:
            try:
                self._websocket.run_forever()
            except Exception as err:
                print(f"Exception in websocket, {err}")
            time.sleep(1)

    def start(self, thread=True):
        """ Start websocket. If thread is True, it will run in a different thread """
        self.connect()
        if thread:
            print(f"Starting websocket connection in a thread")
            self._websocket_thread = threading.Thread(target=self._run_forever)
            self._websocket_thread.daemon = True
            self._websocket_thread.start()
        else:
            self._run_forever()

    def on_message(self, ws, message):
        """ on message callback """
        # print("Receive message. Update option chain")
        # print(message)
        # Get mode of the stream
        mode = get_mode_from_stream(message)
        if mode == FeedModes.MARKET_DATA:
            data = MarketData.create(message)
            self._option_chain.update(data)
        elif mode == FeedModes.COMPACT_MARKETDATA:
            data = CompactMarketData.create(message)
            self._option_chain.update(data)
            print(data)

    def on_open(self, ws):
        """ on open callback """
        print("Connection open")
        self._connected = True

    def on_close(self, ws):
        """ Connection closed """
        print("Connection closed")
        self._connected = False

    def send(self, data, opcode=websocket.ABNF.OPCODE_TEXT):
        """ Send data to web socket api """
        data = json.dumps(data)
        if self._connected:
            self._websocket.send(data=data, opcode=opcode)

    def _send_heartbeat(self):
        """ Send heartbeat in every 10 sec to keep the web socket connection alive """
        data = {"a": FeedAction.HEARTBEAT.value, "v": [], "m": ""}
        while True:
            time.sleep(5)
            self.send(data, opcode=websocket.ABNF.OPCODE_PING)

    def send_heartbeat(self):
        """ Wrapper to run send_heartbeat in thread """
        thread = threading.Thread(target=self._send_heartbeat)
        thread.daemon = True
        thread.start()

    def wait_until_connection_open(self):
        """ Wait till web socket connection is open """
        while not self._connected:
            time.sleep(0.01)

    @property
    def connected(self) -> bool:
        return self._connected
