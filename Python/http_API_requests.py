# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 10:40:26 2017

@author: Maxence
"""

import requests
import queue
import sys
import time
from threading import Thread
from operator import itemgetter


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


lines = [line.rstrip('\n') for line in open('src/API_KEY.password')]
API_KEY = lines[0]
API_SECRET = lines[1]
plateforme={'Bitstamp': 'BITS','Cryptopia':'CPIA','Global Digital Asset Exchange':'GDAE','VBTC':'VBTC','Liqui.io':'LIQU' ,'OKCoin': 'OK', 'Bter': 'BTER','Bitfinex':'BITF','BTC China':'BTCC','Kraken':'KRKN','Poloniex':'PLNX','C-Cex':'CCEX','Huobi':'HUOB','Bittrex':'BTRX','CEX.IO':'CXIO'}


def get_dictionnary():
# Dictionnaire Plateformes (frais de retrait et dépôt)
# plateforme : { crypto : [%,flat,limite/jour] ,... } 
    dictionnaire={
                    'Bitfinex' : {'BTC':[0,0.0005,-1],'ETH':[0,0.01,-1],'BCH':[0,0.0005,-1],'NEO':[0,0,-1],'LTC':[0,0.001,-1],'OMG':[0,0.1,-1],'IOT':[0,0,-1],'ZEC':[0,0.001,-1],'XRP':[0,0.02,-1],'DSH':[0,0.01,-1],'EOS':[0,0.1,-1],'ETC':[0,0.01,-1],'XMR':[0,0.04,-1],'ETP':[0,0.01,-1],'SAN':[0,0.1,-1],'USD':[0,5.0,-1]},
                    'Bitstamp' : {'BTC':[0,0,-1],'XRP':[0,0,-1],'LTC':[0,0,-1],'ETH':[0,0,-1]},
                    'Bittrex' : {'BTC':[0,0.0005,-1],'LTC':[0,0.001,-1],'ETH':[0,0.01,-1],'ETC':[0,0.01,-1],'ZEC':[0,0.001,-1],'XMR':[0,0.04,-1],'DASH':[0,0.01,-1],'XRD':[0,0.02,-1],'EOS':[0,0.1,-1],'SAN':[0,0.1,-1],'OMG':[0,0.1,-1],'BCH':[0,0.0005,-1],'NEO':[0,0,-1],'ETP':[0,0.01,-1]},
                    'BTC China' : {'BTC':[0,0.0015,-1],'LTC':[0,0.001,-1],'ETH':[0,0.01,-1],'BCC':[0,0.0005,-1]},
                    'Bter' : {'USD':[0,0,20000],'CNY':[0.1,2,1000000],'BTC':[0,0.002,20],'BCC':[0,0.0006,500],'LTC':[0,0.02,5000],'ZEC':[0,0.0006,300],'ETH':[0,0.01,5000],'ETC':[0,0.01,50000],'DASH':[1,0.02,500],'QTUM':[0,0.1,30000],'DOGE':[1,5,10000000],'XEM':[1,10,5000000],'IFC':[1,10,300000000],'REP':[0,0.01,2000],'BAT':[0,0.1,200000],'SNT':[0,1,3000000],'BTM':[0,1,3000000],'CVC':[0,1,100000],'DOC':[0,1,1000000],'VEN':[0,1,200000],'LRC':[0,1,20000000],'UBC':[0,1,800000],'OAX':[0,1,10000],'ZRX':[0,1,50000],'PST':[0,1,1000000],'TNT':[0,1,50000],'LLT':[0,1,2000000],'DNT':[0,1,20000],'DPY':[0,1,60000],'STORJ':[0,1,50000],'OMG':[0,0.1,30000],'PAY':[0,0.1,50000],'EOS':[0,0.1,50000],'ICO':[0,0.5,5000000],'HKG':[0,0.01,10000],'TIPS':[1,10,20000000],'NMC':[1,0.001,3000],'NXT':[0.3,1,2000000],'XCP':[1,0.1,50000],'ETP':[0,0.01,200000],'XRP':[0,0.1,100000],'PPC':[1,0.001,10000],'FTC':[1,0.1,100000],'CNC':[1,0.1,500000],'XPM':[1,0.1,50000],'TIX':[1,5,5000000000],'XMR':[1,0.2,1000],'BTS':[1,1,5000000],'XCN':[1,0.1,5000000],'MSC':[1,0.1,50000],'XTC':[1,10,1000000],'SHELL':[0,1,100000],'MG':[0,0.5,10000000]},
                    'C-CEX':{},
                    #WARNING : ONLY VISA WITHDRAWAL https://cex.io/fee-schedule#/tab/payments
                    'CEX.IO':{'USD':[0,3.80,-1],'EUR':[0,3.5,-1],'RUB':[2.5,30,-1],'GBP':[0,2.9,-1]},
                    'Cryptopia':{},
                    'GDAX':{},
                    'HUOBI' : {},
                    'Kraken':{},
                    'Liqui.io':{},
                    'Okcoin':{'USD':[0.1,0,-1],'BTC':[0,0,-1],'LTC':[0,0,-1]},
                    'Poloniex':{},
                    'Vaultoro':{}
                    }
    return dictionnaire 

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


def background_transfer(crypto,plateformA,plateformB,volume):
    dictionnary=get_dictionnary()
    if(volume<dictionnary[plateformA][crypto][2] or dictionnary[plateformA][crypto][2]==-1):
        direct_transfer=volume-(volume)*dictionnary[plateformA][crypto][0]-dictionnary[plateformA][crypto][1]
        tmp=[]
        append=tmp.append
        for key,value in dictionnary[plateformA].items():
            if(key!=crypto):
                exch_fee=0
                for exchanges in get_exchanges():
                    if(exchanges['exch_name']==plateformA):
                        exch_fee+=float(exchanges['exch_fee'])
                ticker=get_one_ticker(plateforme[plateformA],crypto+"/"+key)
                fee=volume*float(ticker[0]['bid'])*float(exch_fee)
                tmp_costA=volume*float(ticker[0]['bid'])-fee-(float(ticker[0]['ask'])-float(ticker[0]['bid']))
                costA=tmp_costA-value[0]*tmp_costA-value[1] #prix de sortie de A ce qui arrive sur B        
                append([key,costA])
            else:
                foo=1
        not_direct=min(tmp,key=itemgetter(1))
        exch_fee=0
        for exchanges in get_exchanges():
            if(exchanges['exch_name']==plateformB):
                exch_fee+=float(exchanges['exch_fee'])    
                break      
        ticker=get_one_ticker(plateforme[plateformB],crypto+"/"+not_direct[0])
        fee=0
        if(float(ticker[0]['bid'])!=0):
            fee+=not_direct[1]*(1/float(ticker[0]['bid']))*float(exch_fee)
        tmp_cost=not_direct[1]*(1/float(ticker[0]['bid']))-fee
        
        coast_total=tmp_cost-((1/float(ticker[0]['ask']))-(1/float(ticker[0]['bid'])))
        return max(direct_transfer,coast_total)
    else:
        return -1
    

def get_money(crypto,exchange):
    return 0

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




