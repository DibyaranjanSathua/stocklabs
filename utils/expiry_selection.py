"""
File:           expiry_selection.py
Author:         Dibyaranjan Sathua
Created on:     27/07/21, 12:26 am
"""
from typing import Optional
import enum
import datetime


class Expiry(enum.IntEnum):
    """ Expiry Types """
    CURRENT_WEEKLY_EXPIRY = 1
    NEXT_WEEKLY_EXPIRY = 2
    CURRENT_MONTHLY_EXPIRY = 3
    NEXT_MONTHLY_EXPIRY = 4


class ExpirySelection:
    """ Get expiry date """
    TODAY: Optional[datetime.date] = None       # Used in back testing

    @staticmethod
    def get_expiry(expiry: Expiry) -> Optional[datetime.date]:
        """ Get the expiry date """
        expiry_date: Optional[datetime.date] = None
        if expiry == Expiry.CURRENT_WEEKLY_EXPIRY:
            expiry_date = ExpirySelection.get_current_weekly_expiry()
        elif expiry == Expiry.NEXT_WEEKLY_EXPIRY:
            expiry_date = ExpirySelection.get_next_weekly_expiry()
        elif expiry == Expiry.CURRENT_MONTHLY_EXPIRY:
            expiry_date = ExpirySelection.get_current_month_expiry()
        elif expiry == Expiry.NEXT_MONTHLY_EXPIRY:
            expiry_date = ExpirySelection.get_next_month_expiry()
        return expiry_date

    @staticmethod
    def get_current_weekly_expiry():
        """ Return coming thursday date """
        today = ExpirySelection.TODAY or datetime.date.today()
        # Monday is 0 and Sunday is 6. Thursday is 3
        offset = (3 - today.weekday()) % 7
        return today + datetime.timedelta(days=offset)

    @staticmethod
    def get_next_weekly_expiry():
        """ Return next week thursday date """
        return ExpirySelection.get_current_weekly_expiry() + datetime.timedelta(days=7)

    @staticmethod
    def get_current_month_expiry():
        """ Return current month last thursday date """
        today = ExpirySelection.TODAY or datetime.date.today()
        # Next month 1st
        year = today.year + (today.month // 12)
        month = today.month % 12 + 1
        next_month_first = datetime.date(year=year, month=month, day=1)
        offset = (next_month_first.weekday() - 3) % 7
        return next_month_first - datetime.timedelta(days=offset)

    @staticmethod
    def get_next_month_expiry():
        """ Return next month last thursday date """
        today = ExpirySelection.TODAY or datetime.date.today()
        # Next to next month 1st
        year = today.year + (today.month // 12)
        month = today.month % 12 + 2
        next_to_next_month_first = datetime.date(year=year, month=month, day=1)
        offset = (next_to_next_month_first.weekday() - 3) % 7
        return next_to_next_month_first - datetime.timedelta(days=offset)
