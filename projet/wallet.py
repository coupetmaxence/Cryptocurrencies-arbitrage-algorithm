# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:18:24 2017

@author: Antoine Vaugeois
"""

from http_API_requests import get_accounts,get_balances,get_markets,add_order,get_order,get_one_ticker,get_balances2,price

#match exchange name and index COINIGY
plateforme={'Bitstamp': 'BITS','Cryptopia':'CPIA','Global Digital Asset Exchange':'GDAE','VBTC':'VBTC','Liqui.io':'LIQU' ,'OKCoin': 'OK', 'Bter': 'BTER','Bitfinex':'BITF','BTC China':'BTCC','Kraken':'KRKN','Poloniex':'PLNX','C-Cex':'CCEX','Huobi':'HUOB','Bittrex':'BTRX','CEX.IO':'CXIO'}
crypto=['BTC','ETH','LTC']

def get_parameters(pair):
    parameters=[]
    append=parameters.append
    for accounts in get_accounts():
        for market in get_markets(plateforme[accounts['exch_name']]):
            print(market)
            if(market['mkt_name']==pair and market['exch_name']==accounts['exch_name'] ):
                for cryp in get_balances(accounts['auth_id']):
                    append([market['exch_name'],accounts['auth_id'],accounts['exch_id'],market['mkt_id'],cryp['balance_curr_code'],cryp['balance_amount_avail'],cryp['last_price']])
    return parameters


# we want to buy/sell at the market price
def limit_price_buy(exchange,market):
    for ticker in get_one_ticker(exchange,market):
        limit_price=ticker['ask']            
    return limit_price

def limit_price_sell(exchange,market):
    for ticker in get_one_ticker(exchange,market):
        limit_price=ticker['bid']            
    return limit_price


def order_quantity(available,percentage): # return the percentage of money that "we can loose" (to define)
    return available*percentage


def price_type_id():
    return 0

def get_money():
    money=0
    get=get_balances2()
    pricee=price()
    for balance in get:
        for prix in pricee:
            if(prix['symbol']==balance['balance_curr_code']):
                money+=float(prix['price_usd'])*float(balance['balance_amount_total'])
    return money
        

print(get_money())
#print(get_parameters('ETH/USD'))
#print(get_balances('122758'))
#print(get_accounts())

#print(add_order('122758','7','2514','1','3','293.74','0.010'))
print(get_order())

#print(limit_price_sell('BITF','USD/ETH'))




