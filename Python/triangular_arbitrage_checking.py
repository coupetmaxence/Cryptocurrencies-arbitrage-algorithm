# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 17:49:48 2017

@author: Maxence COUPET
"""
import requests
import itertools
import numpy as np
from threading import Thread
from multiprocessing import Queue
import time
import csv
import collections


API_KEY = '81c5dac5530270f443bde8dcdb39ef97'
API_SECRET = 'ac50c091e0d83684fdddfb8444ca3e47'

def get_exchanges():
    headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': API_KEY,
            'X-API-SECRET': API_SECRET
            }
    request = requests.request('POST','https://api.coinigy.com/api/v1/exchanges', headers=headers)
    json_data = request.json()['data']
    list_exchanges = []
    for exchange in json_data:
        list_exchanges.append(exchange['exch_code'])
    return list_exchanges

def get_markets(exchange):
    try:
        if(exchange in get_exchanges()):
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
            list_markets = []
            for market in json_data:
                list_markets.append(market['mkt_name'])
            return list_markets
        else:
            return "Invalid exchange"
    except:
        return "Invalid exchange"
    
def get_ticker(exchange, market):
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
        return [True,json_data]
    except:
        print("Error while loading data from server")
        return [False, None]

def list_currencies_market(exchange):
    try:
        markets = get_markets(exchange)
        if markets !="Invalid exchange":
            list_currencies = []
            for market in markets:
                processing = True
                i = 1
                currency1 = market[0:3]
                while processing:
                    if(market[i]=='/'):
                        processing = False
                        currency1 = market[0:i]
                    else:
                        i=i+1
                if(not currency1 in list_currencies):
                    list_currencies.append(currency1)
                
                currency2 = market[i+1:]
                if(not currency2 in list_currencies):
                    list_currencies.append(currency2)
            return [True, markets, list_currencies]
        else:
            return [False, None, None]
    except:
        print("Trouble in list currencies")
        return [False, None, None]


def pairs_matrix(exchange):
    
    # Creating the pairs matrix with -1 
    # -1 represents the fact that the pair doesn't exist in the current exchange
    good_process, markets, list_currencies = list_currencies_market(exchange)
    if good_process:
        currencies_matrix = {(x):{} for x in list_currencies}
        for market in list_currencies:
            currencies_matrix[market] = {(x):[-1,-1] for x in list_currencies}
    
        # Filling the pairs matrix with API datas
        offset = 0
        for x_market in list_currencies:
            # Not a complete matrix just an upper triangular matrix for time optimisation
            for y_market in list_currencies[offset:]:
                if(x_market+"/"+y_market in markets):
                    good_process, ticker = get_ticker(exchange, x_market+"/"+y_market)
                    if good_process and ticker['ask']!=None and ticker['bid']!=None:
                        currencies_matrix[x_market][y_market] = [float(ticker['ask']), float(ticker['bid']),ticker['timestamp']]
                        currencies_matrix[y_market][x_market] = [1/float(ticker['ask']), 1/float(ticker['bid']),ticker['timestamp']]
                elif(y_market+"/"+x_market in markets):
                    good_process, ticker = get_ticker(exchange, y_market+"/"+x_market)
                    if good_process and ticker['ask']!=None and ticker['bid']!=None:
                        currencies_matrix[x_market][y_market] = [1/float(ticker['ask']), 1/float(ticker['bid']),ticker['timestamp']]
                        currencies_matrix[y_market][x_market] = [float(ticker['ask']), float(ticker['ask']),ticker['timestamp']]
                    
            offset = offset + 1
                
        return [True, currencies_matrix, list_currencies]
    else:
        return [False, None, None]

def triangular_combinaison(pairs_matrix, list_currencies):
    list_triplets = []
    offset = 0
    for x_currency in list_currencies:
        for y_currency in list_currencies[offset:]:
            if(pairs_matrix[x_currency][y_currency][0] != -1):
                for temp_currency in list_currencies:
                    if((pairs_matrix[temp_currency][y_currency][0] != -1 or pairs_matrix[y_currency][temp_currency][0] != -1) and (pairs_matrix[temp_currency][x_currency][0] != -1 or pairs_matrix[x_currency][temp_currency][0] != -1) ):
                        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
                        bol = True
                        for _ in list_triplets:
                            if(compare(_,[x_currency, y_currency, temp_currency])):
                                bol = False
                        if(bol):
                            list_triplets.append([x_currency, y_currency, temp_currency])
        offset = offset + 1
    return list_triplets

def triangular_pattern(exchange, pairs_matrix, list_triplets, counter):

    with open("historic_data.csv", "a", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([exchange])
    counter[0] = counter[0] + len(list_triplets)
    for triplet in list_triplets:
        combinaisons = itertools.permutations(triplet)
        list_rates = []
        timestamp = ""
        for combinaison in combinaisons:
            counter[1] = counter[1] + 1
            exchange_rates = []
            
            if(pairs_matrix[combinaison[0]][combinaison[1]][0]==-1):
                exchange_rates.append(1/pairs_matrix[combinaison[1]][combinaison[0]][0])
                timestamp = pairs_matrix[combinaison[1]][combinaison[0]][2]
            else:
                exchange_rates.append(pairs_matrix[combinaison[0]][combinaison[1]][1])
                timestamp = pairs_matrix[combinaison[0]][combinaison[1]][2]
                
            if(pairs_matrix[combinaison[1]][combinaison[2]][0]==-1):
                exchange_rates.append(1/pairs_matrix[combinaison[2]][combinaison[1]][0])
            else:
                exchange_rates.append(pairs_matrix[combinaison[1]][combinaison[2]][1])
        
            if(pairs_matrix[combinaison[2]][combinaison[0]][0]==-1):
                exchange_rates.append(1/pairs_matrix[combinaison[0]][combinaison[2]][0])
            else:
                exchange_rates.append(pairs_matrix[combinaison[2]][combinaison[0]][1])
        
            fee = 0.998
            final_rate = 100*exchange_rates[0]*exchange_rates[1]*exchange_rates[2]*fee**3 -100
            list_rates.append([combinaison[0]+"/"+combinaison[1]+"/"+combinaison[2]+"/"+combinaison[0],final_rate])
            if(final_rate > 5):
                print("Rates : "+str(exchange_rates[0])+" ; "+str(exchange_rates[1])+" ; "+str(exchange_rates[2]))
                counter[2] = counter[2]+1
                print("Combinaison : "+combinaison[0]+"/"+combinaison[1]+"/"+combinaison[2]+"/"+combinaison[0]+" Gain rate :"+str(np.round(final_rate,4))+" %")
        index, value =max_index_value(list_rates)
        if(value>5):
            with open("historic_data.csv", "a", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow([timestamp,list_rates[index][0],np.round(value,4)])

def max_index_value(tab):
    max_value = tab[0][1]
    max_index = 0
    for index, subtab in enumerate(tab):
        if(subtab[1] > max_value):
            max_index= index
            max_value = subtab[1]
    return max_index, max_value


start = time.time()
counter = [0,0,0]
while(True): 
    for exchange in get_exchanges():
        forbidden_exchanges = ["KRKZ"]
        if(not exchange in forbidden_exchanges):
            print("Exchange : "+exchange)
            good_process, currencies_matrix, list_currencies = pairs_matrix(exchange)
            if good_process:
                triplets = triangular_combinaison(currencies_matrix, list_currencies)
                triangular_pattern(exchange, currencies_matrix, triplets, counter)
                print(counter)
                print("Time since beggining : "+ str(time.time()-start))
            else:
                print("Error of processing")

            
input("Press Enter to continue...")
    


    
    
    
