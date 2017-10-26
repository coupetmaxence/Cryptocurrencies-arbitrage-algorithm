# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:02:50 2017

@author: Maxence
"""


from thread_pooling import ThreadPool
from http_API_requests import get_exchanges, get_ticker, get_order_book
import sqlite3
import time


def init_database():
    conn = sqlite3.connect('order_books.db')
    for exchange in get_exchanges():
        try:
            conn.execute('''CREATE TABLE ''' + exchange['exch_code']+'''
                 (paire, timestamp, list_bids, list_asks, mean_price)''')
        except:
            print('error')
    conn.commit()
    conn.close()

def store_order_book(exchange, market):
    conn = sqlite3.connect('order_books.db')
    order_book_data = get_order_book(exchange, market)
    asks = order_book_data['asks']
    bids = order_book_data['bids']
    data = (market, time.time(), bids, asks, 0)
    conn.execute("INSERT INTO "+exchange+" VALUES (?,?,?,?,?)", data)
    conn.commit()
    conn.close()

def get_order_book_db(exchange):
    conn = sqlite3.connect('order_books.db')
    for row in conn.execute('SELECT * FROM '+exchange):
        print(row)
    conn.close()

def order_book_analysis(exchange, market):
    order_book_data = get_order_book(exchange, market)
    asks = order_book_data['asks']
    bids = order_book_data['bids']
    

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


    


print(moove_consequences("BTER", "BTC/CNY", 1, "BUY"))

