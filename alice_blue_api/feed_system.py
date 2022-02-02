"""
File:           feed_system.py
Author:         Dibyaranjan Sathua
Created on:     27/07/21, 2:02 am
"""
from typing import Set, List, Optional
from alice_blue_api.api import AliceBlueApi
from alice_blue_api.websocket import AliceBlueWebSocket
from alice_blue_api.option_chain import OptionChain
from alice_blue_api.enums import OptionType, FeedModes, FeedAction
from alice_blue_api.instruments import Instrument
from alice_blue_api.websocket_streams import CompactMarketData


class FeedSystem:
    """ System to wrap all the APIs and provide methods to subscribe or unsubscribe instruments """
    FEED_MODE = FeedModes.COMPACT_MARKETDATA
    __instance: Optional["FeedSystem"] = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(FeedSystem, cls).__new__(cls, *args, **kwargs)
            return cls.__instance
        raise SyntaxError("This is a Singleton class. Use get_instance() method")

    def __init__(self):
        self._api_handler: AliceBlueApi = AliceBlueApi.get_handler()
        self._web_socket: AliceBlueWebSocket = AliceBlueWebSocket()
        self._option_chain: OptionChain = OptionChain.get_instance()
        # Keep track of the instruments that are subscribed
        self._subscribed_instrument_code: Set[int] = set()
        self._start = False

    @classmethod
    def get_instance(cls):
        """ Get or create feed system """
        if cls.__instance is None:
            cls.__instance = FeedSystem()
        return cls.__instance

    @classmethod
    def reset(cls):
        """ Method for test purposes. Don't use it in real code """
        cls.__instance = None

    def start(self):
        """ Setup API to get the required tokens and start web socket """
        # Check for not to start the web socket streaming multiple times
        if self._start:
            return None
        self._start = True
        self._api_handler.api_setup()
        self._api_handler.nfo_setup()
        self._api_handler.nse_setup()
        self._web_socket.start(thread=True)
        self._web_socket.send_heartbeat()
        self._web_socket.wait_until_connection_open()
        self._subscribe_indices()

    def _subscribe_indices(self):
        """ Subscribe the indices nifty, banknifty and india vix at the start of the feed system """
        self.subscribe(instruments=[
            self._api_handler.nifty_index,
            self._api_handler.banknifty_index,
            self._api_handler.india_vix_index
        ])

    def subscribe(self, instruments: List[Instrument]):
        """ Subscribe the instrument if it is not subscribed """
        # Filter out the instruments that are not subscribed and the code of new instrument to set
        instruments_to_be_subscribed = []
        for instrument in instruments:
            if instrument.code not in self._subscribed_instrument_code:
                self._subscribed_instrument_code.add(instrument.code)
                instruments_to_be_subscribed.append((instrument.exchange_code, instrument.code))
        data = {
            "a": FeedAction.SUBSCRIBE.value,
            "v": instruments_to_be_subscribed,
            "m": self.FEED_MODE.value
        }
        self._web_socket.send(data)

    def unsubscribe(self, instruments: List[Instrument]):
        """ Unsubscribe the instrument if it is subscribed """
        unsubscribe_instruments = []
        for instrument in instruments:
            if instrument.code in self._subscribed_instrument_code:
                self._subscribed_instrument_code.remove(instrument.code)
                unsubscribe_instruments.append((instrument.exchange_code, instrument.code))
        data = {
            "a": FeedAction.UNSUBSCRIBE.value,
            "v": unsubscribe_instruments,
            "m": self.FEED_MODE.value
        }
        self._web_socket.send(data)

    def nifty_index(self) -> CompactMarketData:
        """ Get the current value of nifty index """
        return self._option_chain.get_market_data_by_instrument(self._api_handler.nifty_index)

    def banknifty_index(self) -> CompactMarketData:
        """ Get the current value of banknifty index """
        return self._option_chain.get_market_data_by_instrument(self._api_handler.banknifty_index)

    def india_vix_index(self) -> CompactMarketData:
        """ Get the current value of india vix """
        return self._option_chain.get_market_data_by_instrument(self._api_handler.india_vix_index)

    @property
    def api_handler(self) -> AliceBlueApi:
        return self._api_handler

    @property
    def option_chain(self) -> OptionChain:
        return self._option_chain
