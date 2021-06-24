"""
File:           websocket.py
Author:         Dibyaranjan Sathua
Created on:     20/06/21, 7:36 pm

https://websocket-client.readthedocs.io/en/latest/app.html#websocket._app.WebSocketApp.__init__
"""
from typing import Optional
import json
import websocket


class AliceBlueWebSocket:
    """ Web socket connection to get live feed market data """
    WS_ENDPOINT: str = 'wss://ant.aliceblueonline.com/hydrasocket/v2/websocket' \
                       '?access_token={access_token}'

    def __init__(self, access_token: str):
        self._access_token = access_token
        self._websocket: Optional[websocket.WebSocketApp] = None
        self._connected = False

    def connect(self):
        """ Connect to web socket """
        url = self.WS_ENDPOINT.format(access_token=self._access_token)
        self._websocket = websocket.WebSocketApp(
            url=url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_message=self.on_message
        )
        self._websocket.run_forever()

    def on_message(self, ws, message):
        """ on message callback """
        print("Receive message")
        print(message)

    def on_open(self, ws):
        """ on open callback """
        print("Connection open")
        self._connected = True
        data = {"a": "subscribe", "v": [(2, 52242), (2, 52243)],
                "m": "compact_marketdata"}
        self.send(data)

    def on_close(self, ws):
        """ Connection closed """
        print("Connection closed")
        self._connected = False

    def send(self, data):
        """ Send data to web socket api """
        data = json.dumps(data)
        if self._connected:
            self._websocket.send(data=data)
