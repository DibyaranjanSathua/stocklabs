"""
File:           test_kite_candle.py
Author:         Dibyaranjan Sathua
Created on:     06/07/21, 2:09 am
"""
import datetime
from kite_api import KiteCandle, CandleTimeFrame, InstrumentCandle


def test1():
    bnf_token = 260105
    to_date = datetime.date.today()
    five_days = datetime.timedelta(days=5)
    from_date = to_date - five_days
    kite_candle = KiteCandle()
    kite_candle.send_request(
        instrument_token=bnf_token,
        timeframe=CandleTimeFrame.FIVE_MINUTE,
        to_date=to_date,
        from_date=from_date
    )
    kite_candle.today = datetime.date(year=2021, month=7, day=7)
    if kite_candle.request_successful:
        print("Kite candle API successful")
        today_open_price = kite_candle.get_todays_open_price()
        print(today_open_price)
        high, low = kite_candle.get_previous_trading_day_high_low()
        print(f"High: {high}, Low: {low}")


if __name__ == "__main__":
    test1()
