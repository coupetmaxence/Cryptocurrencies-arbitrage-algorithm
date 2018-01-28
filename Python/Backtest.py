# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 20:54:32 2018

@author: Antoine Vaugeois
"""

import time
import numpy as np
from operator import itemgetter
from simple_arbitrage import get_yield
from http_API_requests import get_money,add_order,get_one_ticker,prices

#simuler le temps de validation d'une transaction par une loi normale 
#paramètres de cette dernière à déterminer
#regarder sur Reddit

def random_number(mu,sigma):
    return np.random(100000)*sigma+mu
        

def backtest(market):
    
    # cash in the wallet
    monney={'BITF':{'BTC':1,'ETH':10,'USD':10000},'BITS':{'BTC':1,'ETH':10,'USD':10000},'CXIO':{'BTC':1,'ETH':10,'USD':10000}}
    #pair=['BITF/BITS','BITF/KRKN','BITF/CXIO','BITS/BITF','BITS/KRKN','BITS/CXIO','KRKN/BITF','KRKN/BITS','KRKN/CXIO','CXIO/BITF','CXIO/BITS','CXIO/KRKN']
    
    btc=0
    eth=1
    usd=2
    begin=0

    for elt,cle in monney.items():
       begin+=cle['BTC']*float(prices()[0]['price_usd'])
       begin+=cle['ETH']*float(prices()[1]['price_usd'])
       begin+=cle['USD']


    market=['BTC/USD','ETH/USD','ETH/BTC']
    buy="ask"
    sell="bid"
    #get datas yields 
    liste=get_yield(market)
    index_market=0
    
    for elt in liste:
        for arbitrage in elt:
            if(arbitrage[2]>3):
                
                plateforme1=arbitrage[1][0:arbitrage[1].find('/',2)] #buy
                plateforme2=arbitrage[1][arbitrage[1].find('/',2)+1:] #sell
                
                price1=get_one_ticker(plateforme1,market[index_market])[0]
                price2=get_one_ticker(plateforme2,market[index_market])[0]
                
                ticker1=market[index_market][0:market[index_market].find('/',2)]
                ticker2=market[index_market][market[index_market].find('/',2)+1:]
                
                amount=monney[plateforme1][ticker1]*0.1
                monney[plateforme1][ticker1]=monney[plateforme1][ticker1]-amount
                monney[plateforme1][ticker2]=monney[plateforme1][ticker2]+amount*float(price1[sell])

                monney[plateforme2][ticker2]=monney[plateforme2][ticker2]-amount*float(price2[buy])
                monney[plateforme2][ticker1]=monney[plateforme2][ticker1]+amount*0.1
                
        index_market+=1
    print(monney)
    after=0
    for elt,cle in monney.items():
       after+=cle['BTC']*float(prices()[0]['price_usd'])
       after+=cle['ETH']*float(prices()[1]['price_usd'])
       after+=cle['USD']
    print(begin)
    print(after)
        
           
           #(pair[0],pair[2][0:pair.find('/',2)])


if __name__=="__main__":
    market=['BTC/USD','ETH/USD','ETH/BTC']
    backtest(market)
    