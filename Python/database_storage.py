# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:20:42 2017

@author: Maxence
"""
import sqlite3

def init_database(list_exchanges):
    conn = sqlite3.connect('order_books.db')
    for exchange in list_exchanges:
        try:
            conn.execute('''CREATE TABLE ''' + exchange['exch_code']+'''
                 (pair, timestamp, highest_bid, lowest_ask, volume, fee)''')
        except:
            print('error')
    conn.commit()
    conn.close()

