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
        

def backtest(market,monney):
    
    # cash in the wallet
    #pair=['BITF/BITS','BITF/KRKN','BITF/CXIO','BITS/BITF','BITS/KRKN','BITS/CXIO','KRKN/BITF','KRKN/BITS','KRKN/CXIO','CXIO/BITF','CXIO/BITS','CXIO/KRKN']

    #monney in the wallet at the beginning    
   


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
                #print(str(ticker1)+" "+str(amount))
                
                #rajouter conditions sur wallet
                if(monney[plateforme1][ticker2]-amount*float(price1[buy])>=0 and monney[plateforme2][ticker1]-amount>=0):
                    monney[plateforme1][ticker1]=monney[plateforme1][ticker1]+amount
                    monney[plateforme1][ticker2]=monney[plateforme1][ticker2]-amount*float(price1[buy])
    
                    monney[plateforme2][ticker2]=monney[plateforme2][ticker2]+amount*float(price2[sell])
                    monney[plateforme2][ticker1]=monney[plateforme2][ticker1]-amount
                
        index_market+=1
    #print(monney)
    
        


if __name__=="__main__":
    market=['BTC/USD','ETH/USD','ETH/BTC']
    monney={'BITF':{'BTC':1,'ETH':10,'USD':10000},'BITS':{'BTC':1,'ETH':10,'USD':10000},'CXIO':{'BTC':1,'ETH':10,'USD':10000}}
    begin=0
    begin_btc=0
    for elt,cle in monney.items():
       begin+=cle['BTC']*float(prices()[0]['price_usd'])
       begin+=cle['ETH']*float(prices()[1]['price_usd'])
       begin+=cle['USD']
       begin_btc=cle['BTC']+cle['USD']/float(prices()[0]['price_usd'])+cle['ETH']*float(prices()[1]['price_btc'])

    print("Monney in the wallets: "+str(round(begin,2))+"$, "+str(round(begin_btc,2))+"BTC.")

    for i in range(0,10):
        backtest(market,monney)
        
        after=0
        after_btc=0
        
        for elt,cle in monney.items():
            after+=cle['BTC']*float(prices()[0]['price_usd'])
            after+=cle['ETH']*float(prices()[1]['price_usd'])
            after+=cle['USD']
            after_btc=cle['BTC']+cle['USD']/float(prices()[0]['price_usd'])+cle['ETH']*float(prices()[1]['price_btc'])
        print("Monney in the wallets: "+str(round(after,2))+"$ , "+str(round(after_btc,2))+"BTC.")
    print(monney)
    