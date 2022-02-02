"""
File:           test_utils.py
Author:         Dibyaranjan Sathua
Created on:     27/07/21, 1:04 am
"""
import datetime
from utils.expiry_selection import Expiry, ExpirySelection


def test_expiry_selection():
    """ Test expiry selection """
    print(f"Today: {datetime.date.today()}")
    print(f"Current week expiry: {ExpirySelection.get_expiry(Expiry.CURRENT_WEEKLY_EXPIRY)}")
    print(f"Next week expiry {ExpirySelection.get_expiry(Expiry.NEXT_WEEKLY_EXPIRY)}")
    print(f"Current month expiry {ExpirySelection.get_expiry(Expiry.CURRENT_MONTHLY_EXPIRY)}")
    print(f"Next month expiry {ExpirySelection.get_expiry(Expiry.NEXT_MONTHLY_EXPIRY)}")

    ExpirySelection.TODAY = datetime.date(year=2021, month=12, day=6)
    print(f"Today: {ExpirySelection.TODAY}")
    print(f"Current week expiry: {ExpirySelection.get_expiry(Expiry.CURRENT_WEEKLY_EXPIRY)}")
    print(f"Next week expiry {ExpirySelection.get_expiry(Expiry.NEXT_WEEKLY_EXPIRY)}")
    print(f"Current month expiry {ExpirySelection.get_expiry(Expiry.CURRENT_MONTHLY_EXPIRY)}")
    print(f"Next month expiry {ExpirySelection.get_expiry(Expiry.NEXT_MONTHLY_EXPIRY)}")


if __name__ == "__main__":
    test_expiry_selection()
