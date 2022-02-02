"""
File:           base_strategy.py
Author:         Dibyaranjan Sathua
Created on:     27/07/21, 1:42 am
"""
from alice_blue_api.feed_system import FeedSystem


class BaseStrategy:
    """ Contains common functions used by other strategies. """
    def __init__(self):
        self._feed_system: FeedSystem = FeedSystem.get_instance()
