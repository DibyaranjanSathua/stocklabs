"""
File:           test_alice_blue_candle.py
Author:         Dibyaranjan Sathua
Created on:     24/07/21, 9:38 pm
"""
import datetime
from alice_blue_api.candle import CandleApi, CandleTimeFrame


def test_bnf(bnf_token, candle_api):
    to_date = datetime.datetime.now()
    five_days = datetime.timedelta(days=5)
    from_date = to_date - five_days
    candle_api.send_request(
        instrument_token=bnf_token,
        timeframe=CandleTimeFrame.FIVE_MINUTE,
        to_date=to_date,
        from_date=from_date
    )
    candle_api.today = datetime.date(year=2021, month=7, day=23)
    if candle_api.request_successful:
        print("AliceBlue candle API successful")
        today_open_price = candle_api.get_todays_open_price()
        print(today_open_price)
        high, low = candle_api.get_previous_trading_day_high_low()
        print(f"High: {high}, Low: {low}")


if __name__ == "__main__":
    bnf_token = 26009       # For bnf index
    candle_api = CandleApi.for_nse_indicies()
    test_bnf(bnf_token, candle_api)

    bnf_token = 53179       # For bnf July fut
    candle_api = CandleApi.for_nfo()
    test_bnf(bnf_token, candle_api)
