"""
File:           strike_selection.py
Author:         Dibyaranjan Sathua
Created on:     20/07/21, 11:10 pm
"""


class StrikeSelection:
    """ Utility function for strike selection """

    @staticmethod
    def get_nearest_100_strike(index):
        """ Get the nearest 100 strike to index """
        return round(index / 100) * 100
