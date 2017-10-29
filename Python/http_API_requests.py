# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 10:40:26 2017

@author: Maxence
"""

import requests
import queue
from threading import Thread
import sys
import time

        ##############################################################################
        #                                                                            #
        #                API From Coinigy                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #                        
        #                                                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #
        ##############################################################################


lines = [line.rstrip('\n') for line in open('API_KEY.password')]
API_KEY = lines[0]
API_SECRET = lines[1]




def get_exchanges():
    try:
        headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': API_KEY,
                'X-API-SECRET': API_SECRET
                }
        request = requests.request('POST','https://api.coinigy.com/api/v1/exchanges', headers=headers)
        json_data = request.json()['data']
        if(json_data!=[None]):
            return json_data
        else:
            return None
    except:
        return None


def get_markets(exchange):
    try:
        values = """
        {
            "exchange_code": """+'"'+exchange+'"'+"""
        }
        """
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': API_KEY,
            'X-API-SECRET': API_SECRET
            }
        request = requests.request('POST','https://api.coinigy.com/api/v1/markets', data=values, headers=headers)
        json_data = request.json()['data']
        return json_data
    except:
        return None


def get_ticker(exchange, market, fee, liste):

   
    try:
        values = """
            {
                "exchange_code": """+'"'+exchange+'"'+""",
                "exchange_market": """+'"'+market+'"'+"""
            }
            """
        headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': API_KEY,
                'X-API-SECRET': API_SECRET
                }
        status = ""
        json_data = 1
        
        # Prevent error 503 for Coinigy servers
        while(status != "200"):
            request = requests.request('POST','https://api.coinigy.com/api/v1/ticker', data=values, headers=headers)
            status = str(request)[11:14]
            
            if(status=="200"):
                json_data = request.json()['data'][0]
        #print([True,json_data])
        if(json_data['ask']!= None):
            spread=float(json_data['ask'])-float(json_data['bid'])
            liste.append([exchange, market, fee, json_data['bid'], json_data['ask'], json_data['current_volume'],json_data['timestamp'],spread])
        
    except:
        foo = 1
        
      
def get_one_ticker(exchange, market):   
    try:
        values = """
            {
                "exchange_code": """+'"'+exchange+'"'+""",
                "exchange_market": """+'"'+market+'"'+"""
            }
            """
        headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': API_KEY,
                'X-API-SECRET': API_SECRET
                }
        request = requests.request('POST','https://api.coinigy.com/api/v1/ticker', data=values, headers=headers)
        json_data=request.json()['data']
        return json_data
    except:
        return 0

        
        
def get_accounts():
    headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': API_KEY,
            'X-API-SECRET': API_SECRET
            }
    request = requests.request('POST','https://api.coinigy.com/api/v1/accounts', headers=headers)
    json_data=request.json()['data']
    return json_data
 
def get_balances(auth_ids):
    values = """
    {
         "show_nils": 0,
         "auth_ids":  """+'"'+auth_ids+'"'+"""
     }
    """
    headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': API_KEY,
            'X-API-SECRET': API_SECRET
            }
    request = requests.request('POST','https://api.coinigy.com/api/v1/balances', data=values, headers=headers)
    json_data=request.json()['data']
    return json_data
def get_balances2():
    headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': API_KEY,
            'X-API-SECRET': API_SECRET
            }
    request = requests.request('POST','https://api.coinigy.com/api/v1/balances', headers=headers)
    json_data=request.json()['data']
    return json_data


        ##############################################################################
        #                 Parameters for add_order                                   #
        #                                                                            #
        # 1. auth_id : Numeric ID for API Account                                    #
        # 2. exch_id : ID of Exchange                                                #
        # 3. mkt_id : ID of Market                                                   #
        # 4. order_type_id : Order type from orderTypes API call                     #
        # 5. price_type_id : Price type from orderTypes API call                     #
        #        1:Buy 2:Sell 3:Limit 4:Stop (Limit) 8:Limit (Margin)                #                        
        #        9:Stop Limit(Margin)                                                #
        # 6. limit_price : Buy/Sell Price                                            #
        # 7. stop_price : Price to trigger a stop price type                         #
        # 8. order_quantity :Quantity for order                                      #
        ##############################################################################

def add_order(auth_id,exch_id,mkt_id,order_type_id,price_type_id,limit_price,order_quantity):
    values = """
    {
         "auth_id": """+auth_id+""",
         "exch_id": """+exch_id+""",
         "mkt_id": """+mkt_id+""",
         "order_type_id": """+order_type_id+""",
         "price_type_id": """+price_type_id+""",
         "limit_price": """+limit_price+""",
         "order_quantity": """+order_quantity+"""
     }
    """
    
    headers = {
           'Content-Type': 'application/json',
           'X-API-KEY': API_KEY,
           'X-API-SECRET': API_SECRET
           }
    request = requests.request('POST','https://api.coinigy.com/api/v1/addOrder', data=values, headers=headers)
    order_id = request.json()['data']['internal_order_id']
    confirmation = confirmation_order(order_id, time.time())
    return confirmation, order_id
        

def get_order():
    headers = {
           'Content-Type': 'application/json',
           'X-API-KEY': API_KEY,
           'X-API-SECRET': API_SECRET
           }
    request = requests.request('POST','https://api.coinigy.com/api/v1/orders', headers=headers)
    json_data=request.json()['data']
    return json_data

def get_order_book(exchange, market):
    values = """
    {
         "exchange_code": """+'"'+exchange+'"'+""",
         "exchange_market": """+'"'+market+'"'+""",
         "type": "orders"
    }
    """
    headers = {
           'Content-Type': 'application/json',
           'X-API-KEY': API_KEY,
           'X-API-SECRET': API_SECRET
           }
    request = requests.request('POST','https://api.coinigy.com/api/v1/data', data=values, headers=headers)
    json_data=request.json()['data']
    return json_data


def liste_pair(): # return all trading pair in the market
    liste_id=[]
    append=liste_id.append
    for i in get_exchanges():
        if(int(i['exch_trade_enabled'])==1):
            append(i['exch_id'])
    liste=[]
    append=liste.append
    for i in get_markets():
        if(i['mkt_name'] not in liste and i['exch_id'] in liste_id):
            append(i['mkt_name'])
    return liste

def confirmation_order(order_id, timestamp):
    condition = False
    while(condition== False and time.time()-timestamp < 10):
        book_order = get_order()
        for order in book_order['order_history']:
            if(int(order['order_id'])==order_id):
                print('ok')
                if(order['order_status']=='Executed'):
                    condition = True
    return condition



        ##############################################################################
        #                                                                            #
        #                API From CoinMarketCap                                      #
        #                                                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #                        
        #                                                                            #
        #                                                                            #
        #                                                                            #
        #                                                                            #
        ##############################################################################

def prices():
    request = requests.request('GET','https://api.coinmarketcap.com/v1/ticker/')
    return request.json()




