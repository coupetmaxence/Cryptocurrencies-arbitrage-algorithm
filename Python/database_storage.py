# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:20:42 2017

@author: Maxence
"""
from thread_pooling import ThreadPool
from http_API_requests import get_exchanges, get_ticker, get_order_book, get_markets
import sqlite3

def init_database(list_exchanges):
    conn = sqlite3.connect('order_books.db')
    for exchange in list_exchanges:
        try:
            conn.execute('''CREATE TABLE ''' + exchange+'''
                 (pair, timestamp, highest_bid, lowest_ask, volume, fee)''')
        except:
            print('error')
    conn.commit()
    conn.close()

def store_data(exchange, market):
    conn = sqlite3.connect('order_books.db')
    for exchange in list_exchanges:
        try:
            
            data = (market, time.time(), bids, asks, 0)
            conn.execute("INSERT INTO "+exchange+" VALUES (?,?,?,?,?)", data)
        except:
            print('error')
    conn.commit()
    conn.close()
litst = []
fee = 0.02
get_ticker("BITF", "BTC/USD", fee, litst)
print(litst)

