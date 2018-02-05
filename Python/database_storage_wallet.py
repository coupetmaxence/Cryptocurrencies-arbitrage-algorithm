# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 21:47:28 2018

@author: antoi
"""


import sqlite3
import pandas as pd


class BDD:
    
    """
    This class is representing a database. All the following functions
    allows to create a database, insert datas into it, and get datas as
    different datatypes.
    """
    
    def __init__(self,BDD):
        
        """
        Just defining the name of the database in order to retrieve it later.
        """
        self.Name_BDD=BDD
            
    def create_table(self, Name_Table):
        
        """
        Allows the user to create a database with a specified name.
        If a table with a similar name already exists, an error message
        will be displayed.
        """
        
        try:
            conn=sqlite3.connect(self.Name_BDD)
            cursor=conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS"""+'"'+Name_Table+'"'+"""(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Volume_A REAL,
            Volume_B REAL,
            Price_A REAL,
            Price_B REAL,
            Wallet_A TEXT,
            Wallet_B TEXT
            )        
            """)
            conn.commit()
        except sqlite3.OperationalError:
            print('Error : the table already exists')
        except Exception as e:
            print("Error")
            conn.rollback()
            raise e
        finally:
            conn.close()
    
        
            
    def insert_data(self, data, Name_Table):
        
        """
        Insert specific datas in a specific database.
        Datas must be list of lists like this following :
                [(Date, Open, Close, High, Low, Volume), ...]
        """
        
        conn=sqlite3.connect(self.Name_BDD)
        cursor=conn.cursor()
        cursor.executemany("""
        INSERT OR REPLACE INTO """+'"'+Name_Table+'"'+"""
        (Volume_A, Volume_B,Price_A,Price_B,Wallet_A,Wallet_B) VALUES(?, ?, ?, ?, ?, ?)""", data)
        cursor.execute("""DELETE FROM """+'"'+Name_Table+'"'+""" WHERE rowid NOT IN (SELECT min(rowid) FROM """+Name_Table+""" GROUP BY date, open, close, high, low, volume);""")
        conn.commit()
        
    def get_data_bdd_as_array(self,Name_Table):
        try:
            conn=sqlite3.connect(self.Name_BDD)
            cursor=conn.cursor()
            req="SELECT date, open, high, low, volume FROM "+Name_Table+" ORDER BY date"
            cursor.execute(req)
        except Exception as e:
            print("Error")
            conn.rollback()
            raise e
        rows=cursor.fetchall()
        liste=[]
        append=liste.append
        for row in rows:
            tmp=[]
            for j in range(1,7):
                tmp.append(row[j])
            append(tmp)
        return liste

    def get_data_bdd_as_df(self,Name_Table):
        try:
            conn=sqlite3.connect(self.Name_BDD)
            df=pd.read_sql_query("SELECT date, open, close, high, low, volume FROM "+Name_Table+" ORDER BY date",conn)
        except Exception as e:
            print("Erreur")
            raise e
        return df

  