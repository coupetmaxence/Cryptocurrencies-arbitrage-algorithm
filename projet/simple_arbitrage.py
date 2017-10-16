# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:50:23 2017

@author: Antoine Vaugeois
"""
import xlsxwriter
import xlrd
import os
import openpyxl 
from operator import itemgetter
from thread_pooling import ThreadPool
from http_API_requests import get_exchanges, get_ticker


def price_fee(liste): # return the following list [exchange,bis,ask,timestamp,volume,spread] with the fee apply to the bid and the ask
    price=[]
    append=price.append
    for i in range (len(liste)):
         tmpb=float(liste[i][3])-float(liste[i][3])*float(liste[i][2])
         tmph=float(liste[i][4])+float(liste[i][4])*float(liste[i][2])
         append([liste[i][0],tmpb,tmph,liste[i][6],liste[i][5],liste[i][7]])
    return price

def get_posibility(price): # return the following list [timestamp,exchange A/B,yield,volumeA,volumeB,spreadA,spreadB]
    liste=[] 
    append=liste.append
    for i in range (0,len(price)) :
        for j in range (0,len(price)) :
            if(i!=j and price[i][1]<price[j][1]): # we need to compare the bid (it's a choice you can do the same think with the ask)
                date=price[i][3]
                plateforme=price[i][0]+"/"+price[j][0]
                rendement=((price[j][1]-price[i][2])/price[j][1])*100
                volumeA=price[i][4]
                volumeB=price[j][4]
                if(float(volumeA)>0 and float(volumeB)>0):
                    append([date,plateforme,rendement,volumeA,volumeB,price[i][5],price[j][5]])
    return liste

def write_csv(market,liste):
    if(os.path.exists('arbitrage.xlsx') is True): # if the file exist we open it and write information in the appropriate sheet
        index_market=0
        for j in liste:
            pair=market[index_market]
            wb=xlrd.open_workbook('arbitrage.xlsx')
            sh=wb.sheet_by_name(pair.replace("/","_"))
            index_ligne=0
            for rownum in range(sh.nrows):
                index_ligne+=1
            wb2=openpyxl.load_workbook('arbitrage.xlsx')
            sheet=wb2[pair.replace("/","_")]
            index_market+=1
            index=index_ligne+2
            for i in j:
                a=str(i[0])
                b=str(i[1])
                c=float(i[2])
                d=float(i[3])
                e=float(i[4])
                f=float(i[5])
                g=float(i[6])
                sheet['A'+str(index)]=a
                sheet['B'+str(index)]=b
                sheet['C'+str(index)]=c
                sheet['D'+str(index)]=d
                sheet['E'+str(index)]=e
                sheet['F'+str(index)]=f
                sheet['G'+str(index)]=g
                index+=1 
            wb2.save('arbitrage.xlsx')
    else:         # else we create the file and for each pair in the list we create a sheet with the value of each list inside the liste
        wb=xlsxwriter.Workbook('arbitrage.xlsx')
        bold = wb.add_format({'bold': 1})
        index_market=0
        for j in liste:
            pair=market[index_market]
            worksheet=wb.add_worksheet(pair.replace("/","_"))
            worksheet.write(0,0,'Date',bold)
            worksheet.write(0,1,'Plateforme A/B',bold)
            worksheet.write(0,2,'Rendement',bold)
            worksheet.write(0,3,'Volume A',bold)
            worksheet.write(0,4,'Volume B',bold)
            worksheet.write(0,5,'Spread A',bold)
            worksheet.write(0,6,'Spread B',bold)  
            index_market+=1
            index=1
            for i in j:
                a=str(i[0])
                b=str(i[1])
                c=float(i[2])
                d=float(i[3])
                e=float(i[4])
                f=float(i[5])
                g=float(i[6]) 
                worksheet.write_string(index,0,a)
                worksheet.write_string(index,1,b)
                worksheet.write_number(index,2,c)
                worksheet.write_number(index,3,d)
                worksheet.write_number(index,4,e)
                worksheet.write_number(index,5,f)
                worksheet.write_number(index,6,g) 
                index+=1
    


if __name__ == "__main__":
    #,'ETH/BTC','LTC/USD','LTC/BTC','ETC/BTC','ETC/ETH','XMR/USD','XMR/BTC','DASH/USD','DASH/BTC']
    #market=['$$$/BTC', '1337/BTC', '1ST/BTC', '1ST/ETH','1ST/USDT', '21M/BTC', '2GIVE/BTC', '300/BTC', '42/BTC', '4CHN/BTC', '611/BTC', '808/BTC', '888/BTC', '8BIT/BTC', '9COIN/BTC', 'ABC/BTC', 'ABY/BTC', 'AC/BTC', 'ACC/BTC', 'ACOIN/BTC', 'ACP/BTC', 'ADC/BTC', 'ADCN/BTC', 'ADL/BTC', 'ADST/BTC', 'ADT/BTC', 'ADT/ETH', 'ADX/BTC', 'ADX/ETH', 'ADX/USDT', 'AE/BTC', 'AE/ETH', 'AE/USDT', 'AEON/BTC', 'AGRS/BTC', 'AIB/BTC', 'ALEX/BTC', 'ALL/BTC', 'ALT/BTC', 'AMP/BTC', 'ANI/BTC', 'ANS/BTC', 'ANT/BTC', 'ANT/ETH', 'ANT/USDT', 'APC/BTC', 'APW/BTC', 'APX/BTC', 'ARC/BTC', 'ARCO/BTC', 'ARDR/BTC', 'ARG/BTC', 'ARGUS/BTC', 'ARI/BTC', 'ARK/BTC', 'ARK/USDT', 'ARV/BTC', 'ATH/BTC', 'ATMS/BTC', 'ATOM/BTC', 'AU/BTC', 'AUR/BTC', 'AURS/BTC', 'B3/BTC', 'B@/BTC', 'BASH/BTC', 'BAT/BTC', 'BAT/CNY', 'BAT/ETH', 'BAT/USDT', 'BAY/BTC', 'BBP/BTC', 'BCAP/BTC', 'BCAP/ETH', 'BCAP/USDT', 'BCC/BTC', 'BCC/CNY', 'BCC/ETH', 'BCC/USD', 'BCC/USDT', 'BCF/BTC', 'BCH/BTC', 'BCH/ETH', 'BCH/EUR', 'BCH/GBP', 'BCH/USD', 'BCH/USDT', 'BCH/XBT', 'BCN/BTC', 'BCU/BTC', 'BCU/USD', 'BCY/BTC', 'BDL/BTC', 'BEE/BTC', 'BEEZ/BTC', 'BENJI/BTC', 'BERN/BTC', 'BEST/BTC', 'BHC/BTC', 'BIOS/BTC', 'BIP/BTC', 'BITB/BTC', 'BITCF/BTC', 'BITS/BTC', 'BIZ/BTC', 'BKCAT/BTC', 'BLC/BTC', 'BLITZ/BTC', 'BLK/BTC', 'BLOCK/BTC', 'BMC/BTC', 'BMC/ETH', 'BMC/USDT', 'BNC/BTC', 'BNT/BTC', 'BNT/ETH', 'BNT/USDT', 'BNX/BTC', 'BOLI/BTC', 'BOP/BTC', 'BOPT/BTC', 'BOST/BTC', 'BQ/BTC', 'BRIT/BTC', 'BRK/BTC', 'BRO/BTC', 'BRX/BTC', 'BSD/BTC', 'BSD/USDT', 'BSDB/BTC', 'BSTY/BTC', 'BTA/BTC', 'BTB/BTC', 'BELA/BTC', 'BTCD/BTC', 'BTM/BTC', 'BTS/BTC', 'BURST/BTC', 'CLAM/BTC', 'BTC/CNY', 'CVC/BTC', 'DASH/BTC', 'DCR/BTC', 'DGB/BTC', 'DOGE/BTC', 'EMC2/BTC', 'ETC/BTC', 'ETH/BTC', 'BTC/EUR', 'EXP/BTC', 'FCT/BTC', 'FLDC/BTC', 'FLO/BTC', 'GAME/BTC', 'GAS/BTC', 'BTC/GBP', 'GNO/BTC', 'GNT/BTC', 'BTC/GOLD', 'GRC/BTC', 'HUC/BTC', 'LBC/BTC', 'LSK/BTC', 'LTC/BTC', 'MAID/BTC', 'NAUT/BTC', 'NAV/BTC', 'NEOS/BTC', 'NMC/BTC', 'NOTE/BTC', 'NXC/BTC', 'NXT/BTC', 'OMG/BTC', 'OMNI/BTC', 'PASC/BTC', 'PINK/BTC', 'POT/BTC', 'PPC/BTC', 'RADS/BTC']
    #print(len(market))
    market=['BTC/USD','ETH/USD','ETH/BTC','LTC/USD','LTC/BTC','ETC/BTC','ETC/ETH','XMR/USD','XMR/BTC','DASH/USD','DASH/BTC']
    import time
        
    # Function to be executed in a thread
    ti = time.time()
    # Instantiate a thread pool with 5 worker threads
    pool = ThreadPool(30)

    # On boucle 3 fois les paires
    for i in range(1):
        t=time.time()
        all_list=[]
        for pair in market:
            
            liste = []
            
            for exchange in get_exchanges():
                if(exchange!=None and int(exchange['exch_trade_enabled'])==1 ):
                    pool.add_task(get_ticker, exchange['exch_code'], pair,exchange['exch_fee'], liste)
                else:
                    continue 
            pool.wait_completion()
            price=price_fee(liste)
            cross_possibility=get_posibility(price)
            cross_possibility=sorted(cross_possibility, key=itemgetter(2),reverse=True)
            all_list.append(cross_possibility) 
        write_csv(market,all_list)
        if(time.time()-t<60):
            print("je dors pendant :"+str(60-time.time()+t)+" s")
            time.sleep(60-time.time()+t)
        print("Time of execution : " +str(time.time()-ti))
