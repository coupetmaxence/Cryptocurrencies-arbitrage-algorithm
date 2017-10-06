# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 11:22:39 2017

@author: Maxence
"""

import sys
IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    from Queue import Queue
else:
    from queue import Queue

from threading import Thread


import requests
liste=[]
API_KEY = '5320d6b526c11b208e080eebda4f48f0'
API_SECRET = '54fd25bd7fb901099b74dcbed4f8dc0e'


def get_exchanges():
    headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': API_KEY,
            'X-API-SECRET': API_SECRET
            }
    request = requests.request('POST','https://api.coinigy.com/api/v1/exchanges', headers=headers)
    json_data = request.json()['data']
    return json_data

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

def get_ticker(exchange, market, fee):
    global liste
    #while bool_var:
    var_bool = True
    
    if(var_bool):
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
                    print(request.json())
                    json_data = request.json()['data'][0]
            #print([True,json_data])
            if(json_data['ask']!= None):
                liste.append([exchange, market, fee, json_data['bid'], json_data['ask'], json_data['current_volume']])
            
        except:
            print("Error while loading data from server")
        

class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()


if __name__ == "__main__":
    import time

    # Function to be executed in a thread
   
    # Instantiate a thread pool with 5 worker threads
    pool = ThreadPool(20)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    ti = time.time()
    for exchange in get_exchanges():
        pool.add_task(get_ticker, exchange['exch_code'], "BTC/USD",exchange['exch_fee'])
    pool.wait_completion()
    print("Time : "+str(time.time()-ti))
    print(liste)