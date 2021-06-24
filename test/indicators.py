"""
File:           indicators.py
Author:         Dibyaranjan Sathua
Created on:     20/03/21, 12:26 pm
"""
from indicators.momentum import RSIIndicator

close_price = [518.1, 650.4, 650.4, 650.4, 650.4, 650.4]
indicator = RSIIndicator(close=close_price, period=5, initial=True)
rsi, gain, loss = indicator.calc()
del indicator
print(rsi)


indicator = RSIIndicator(close=[633, 518.1], period=5, prev_avg_gain=gain, prev_avg_loss=loss)
rsi, gain, loss = indicator.calc()
del indicator
print(rsi)


indicator = RSIIndicator(close=[633, 633], period=5, prev_avg_gain=gain, prev_avg_loss=loss)
rsi, gain, loss = indicator.calc()
del indicator
print(rsi)


indicator = RSIIndicator(close=[687.4, 633], period=5, prev_avg_gain=gain, prev_avg_loss=loss)
rsi, gain, loss = indicator.calc()
del indicator
print(rsi)


indicator = RSIIndicator(close=[687.55, 687.4], period=5, prev_avg_gain=gain, prev_avg_loss=loss)
rsi, gain, loss = indicator.calc()
del indicator
print(rsi)


indicator = RSIIndicator(close=[607.6, 687.55], period=5, prev_avg_gain=gain, prev_avg_loss=loss)
rsi, gain, loss = indicator.calc()
del indicator
print(rsi)


indicator = RSIIndicator(close=[506.05, 607.6], period=5, prev_avg_gain=gain, prev_avg_loss=loss)
rsi, gain, loss = indicator.calc()
del indicator
print(rsi)
