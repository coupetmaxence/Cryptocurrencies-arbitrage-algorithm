# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 17:49:48 2017

@author: Maxence COUPET
"""
import requests
import itertools
import numpy as np

API_KEY = 'cb4cb45b2e8ce8111f976868bde66a9d'
API_SECRET = '1e110807c6ea9f6042a70a271dff681b'

# Returns the complete list of exchanges available ex: KRKN for Kraken, BITF for Bitfinex
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

# Returns the complete list of markets for a given exchange ex : BTC/USD
def get_markets(exchange):
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

# Returns various ticker infos on a specific market from a specific exchange (bid/ask price, last trade price, volume)
def get_ticker(exchange, market):
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
    return(json_data)

# Returns a simple list of currencies available on a given exchange ex : EUR, BTC,... (no pairs here)
def list_currencies_market(exchange):
    markets = get_markets(exchange)
    list_currencies = []
    for market in markets:
        currency1 = market[0:3]
        if(not currency1 in list_currencies):
            list_currencies.append(currency1)
        
        currency2 = market[4:8]
        if(not currency2 in list_currencies):
            list_currencies.append(currency2)
    return markets, list_currencies

# Returns an upper-triangular matrix with the exchange rate
def pairs_matrix(exchange):
    
    # Creating the pairs matrix with -1 
    # -1 represents the fact that the pair doesn't exist in the current exchange
    markets, list_currencies = list_currencies_market(exchange)
    
    currencies_matrix = {(x):{} for x in list_currencies}
    for market in list_currencies:
        currencies_matrix[market] = {(x):[-1,-1] for x in list_currencies}

    # Filling the pairs matrix with API datas
    offset = 0
    for x_market in list_currencies:
        # Not a complete matrix just an upper triangular matrix for time optimisation
        for y_market in list_currencies[offset:]:
            if(x_market+"/"+y_market in markets):
                ticker = get_ticker(exchange, x_market+"/"+y_market)
                currencies_matrix[x_market][y_market] = [float(ticker['ask']), float(ticker['bid'])]
                currencies_matrix[y_market][x_market] = [1/float(ticker['ask']), 1/float(ticker['bid'])]
            elif(y_market+"/"+x_market in markets):
                ticker = get_ticker(exchange, y_market+"/"+x_market)
                currencies_matrix[x_market][y_market] = [1/float(ticker['ask']), 1/float(ticker['bid'])]
                currencies_matrix[y_market][x_market] = [float(ticker['ask']), float(ticker['bid'])]
        offset = offset + 1
            
    return [currencies_matrix, list_currencies]

# Returns a list of all the combinaisons of triplets available on an exchange
def triangular_combinaison(pairs_matrix, list_currencies):
    list_triplets = []
    offset = 0
    for x_currency in list_currencies:
        for y_currency in list_currencies[offset:]:
            if(pairs_matrix[x_currency][y_currency][0] != -1):
                for temp_currency in list_currencies:
                    if((pairs_matrix[temp_currency][y_currency][0] != -1 or pairs_matrix[y_currency][temp_currency][0] != -1) and (pairs_matrix[temp_currency][x_currency][0] != -1 or pairs_matrix[x_currency][temp_currency][0] != -1) ):
                        list_triplets.append([x_currency, y_currency, temp_currency])
        offset = offset + 1
    return list_triplets

# Find arbitrage and print it if it's a success
def triangular_pattern(pairs_matrix, list_triplets):
    profitable_counter = 0
    non_profitable_counter = 0
    for triplet in list_triplets:
        combinaisons = itertools.permutations(triplet)
        for combinaison in combinaisons:
            exchange_rates = []
            if(pairs_matrix[combinaison[0]][combinaison[1]][0]==-1):
                exchange_rates.append(1/pairs_matrix[combinaison[1]][combinaison[0]][1])
            else:
                exchange_rates.append(pairs_matrix[combinaison[0]][combinaison[1]][1])
                
            if(pairs_matrix[combinaison[1]][combinaison[2]][0]==-1):
                exchange_rates.append(1/pairs_matrix[combinaison[2]][combinaison[1]][1])
            else:
                exchange_rates.append(pairs_matrix[combinaison[1]][combinaison[2]][1])
        
            if(pairs_matrix[combinaison[2]][combinaison[0]][0]==-1):
                exchange_rates.append(1/pairs_matrix[combinaison[0]][combinaison[2]][0])
            else:
                exchange_rates.append(pairs_matrix[combinaison[2]][combinaison[0]][0])
        
            fee = 0.998
            final_rate = 100*exchange_rates[0]*exchange_rates[1]*exchange_rates[2]*fee**3 -100
            if(final_rate > 0):
                print("Combinaison : "+combinaison[0]+"/"+combinaison[1]+"/"+combinaison[2]+"/"+combinaison[0]+" Gain rate :"+str(np.round(final_rate,4))+" %")
    




for exchange in get_exchanges():
    if(exchange!="KRKN" and exchange!="BTRX"):
        print("Exchange : "+exchange)
        pairs_result = pairs_matrix(exchange)
        triplets = triangular_combinaison(pairs_result[0], pairs_result[1])
        triangular_pattern(pairs_result[0], triplets)
    
            

    


    
    
    
