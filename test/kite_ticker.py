"""
File:           kite_ticker.py
Author:         Dibyaranjan Sathua
Created on:     06/04/21, 12:56 am
"""
import json

directory = "/Users/dibyaranjan/Stocks/data_5thApr/"

last_price = []
close = []
openp = []
low = []
high = []
tradable = []
average = []
for i in range(119, 216):
    file = f"{directory}/data{i}.json"
    with open(file) as fh:
        data = json.load(fh)
    last_price.append(data[0]["last_price"])
    close.append(data[0]["ohlc"]["close"])
    openp.append(data[0]["ohlc"]["open"])
    low.append(data[0]["ohlc"]["low"])
    high.append(data[0]["ohlc"]["high"])
    tradable.append(data[0]["tradable"])
    average.append(data[0][""])


import pdb; pdb.set_trace()
