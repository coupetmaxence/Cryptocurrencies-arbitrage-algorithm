# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:02:50 2017

@author: Maxence
"""


from thread_pooling import ThreadPool
from http_API_requests import get_exchanges, get_ticker, get_order_book

def moove_consequences(exchange, market, volume, order_type):
    order_book_data = get_order_book(exchange, market)
    # we want to fill the order book, so when we are buying, we're matching the ask prices
    data = [];
    if(order_type == "BUY"):
        data = order_book_data['asks']
    else:
        data = order_book_data['bids']
    double_sum = 0.0
    volume_left = volume
    worst_price = 0.0
    best_price = float(data[0]['price'])
    for sub_element in data:
        if(volume_left > 0):
            if(volume_left > float(sub_element['quantity'])):
                double_sum += float(sub_element['total'])
                volume_left -= float(sub_element['quantity'])
                worst_price = float(sub_element['price'])
            else:
                double_sum += float(sub_element['price'])*volume_left
                volume_left = 0
                worst_price = float(sub_element['price'])
    percentage_moove = round(100*float((worst_price-best_price)/worst_price),4)
    return [round(double_sum/volume,4), best_price, worst_price, percentage_moove]


    


print(moove_consequences("BITF", "BTC/USD", 100, "SELL"))
