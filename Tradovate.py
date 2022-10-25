import pandas as pd
import configparser
import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
from datetime import date
from flask import Flask, request, jsonify, render_template, Response
from tda import auth, client
from td.client import TDClient
import os, json, datetime, math
import os, json, requests
import numpy as np
import pandas as pd
import datetime as dt
import time
from datetime import datetime



################
#Tradovate API

API = 	"demo.tradovateapi.com/v1"
ACCOUNT_ID = "vvnsreddy@gmail.com"
ACCOUNTS_PATH = f"/auth/accessTokenRequest"

# get token
headers = {
         "name": "vvnsreddy@gmail.com",
         "password": "Intel123$",
         "appId": "Sample App",
         "appVersion": "1.0",
         "cid": '1133',
         "sec": '66e4c947-0fe2-46b2-b76a-3ed88601ccd8'
}





################

format = ''



def re(integ):
    if len(list(integ)) == 1: return '0'+str(integ)
    else: return str(integ)

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type, exchange):
    #print('TRADOVATE order')
    print(ticker, order_type, qty, round(price), position_type, exchange)
    # get token
    headers = {
        "name": "vvnsreddy@gmail.com",
        "password": "Intel123$",
        "appId": "Sample App",
        "appVersion": "1.0",
        "cid": '1133',
        "sec": '66e4c947-0fe2-46b2-b76a-3ed88601ccd8'
    }

    response = requests.post("https://" + API + ACCOUNTS_PATH, params=headers)
    ACCESS_TOKEN = response.json()['accessToken']
    #print(ACCESS_TOKEN)
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
    if order_type == "BUY_TO_OPEN":
        body = {
            "accountSpec": "DEMO485096",
            "accountId": '1083577',
            "action": "Buy",
            "symbol": "ESZ2",
            "orderQty": '1',
            "orderType": "Market",
            "isAutomated": "true"
        }
        response = requests.post("https://"+API+'/order/placeorder', headers=headers, data=body)
        #print(response.json())

    elif order_type == "SELL_TO_OPEN":
        body = {
            "accountSpec": "DEMO485096",
            "accountId": '1083577',
            "action": "Sell",
            "symbol": "ESZ2",
            "orderQty": '1',
            "orderType": "Market",
            "isAutomated": "true"
        }
        response = requests.post("https://"+API+'/order/placeorder', headers=headers, data=body)
        #print(response.json())
    elif order_type == "SELL_TO_CLOSE":
        body = {
            "accountSpec": "DEMO485096",
            "accountId": '1083577',
            "action": "Sell",
            "symbol": "ESZ2",
            "orderQty": '1',
            "orderType": "Market",
            "isAutomated": "true"
        }
        response = requests.post("https://"+API+'/order/placeorder', headers=headers, data=body)
        #print(response.json())
    elif order_type == "BUY_TO_CLOSE":
        body = {
            "accountSpec": "DEMO485096",
            "accountId": '1083577',
            "action": "Buy",
            "symbol": "ESZ2",
            "orderQty": '1',
            "orderType": "Market",
            "isAutomated": "true"
        }
        response = requests.post("https://"+API+'/order/placeorder', headers=headers, data=body)
        #print(response.json())
        print()





headers = {
    "name": "vvnsreddy",
    "password": "Intel123$",
    "appId": "Sample App",
    "appVersion": "1.0",
    "cid": '1133',
    "sec": '66e4c947-0fe2-46b2-b76a-3ed88601ccd8'
}

response = requests.post("https://" + API + ACCOUNTS_PATH, params=headers)
print(response.json())
ACCESS_TOKEN = response.json()['accessToken']
EXP_TIMEOF_TOKEN = response.json()['expirationTime']
print(response.json())
headers = {
    "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
}

# find any existing positions
#response = requests.post("https://" + API + '/position/list', headers=headers)
#print(response.json())


    # while True:
    #     headers = {
    #         "name": "vvnsreddy@gmail.com",
    #         "password": "Intel123$",
    #         "appId": "Sample App",
    #         "appVersion": "1.0",
    #         "cid": '1133',
    #         "sec": '66e4c947-0fe2-46b2-b76a-3ed88601ccd8'
    #     }
    #     response = requests.post("https://" + API + ACCOUNTS_PATH, params=headers)
    #     ACCESS_TOKEN = response.json()['accessToken']
    #     headers = {
    #         "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    #     }
    #     time.sleep(60*600) # this is in seconds, so 60 seconds x 30 mins



OrderID = 4919403020



# STOP LIMIT SELL
body = {
    "masterid": OrderID
}
ticker = "MESZ2"
response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
# print(response.json())
if ticker == "MESZ2":
    order_price = (response.json()[0]['price']) - 20
else:
    order_price = (response.json()[0]['price']) - 40
print(order_price)

body = {
    "accountSpec": "DEMO485096",
    "accountId": 1083577,
    "action": "Buy",
    "symbol": ticker,
    "orderQty": 1,
    "orderType": "Limit",
    "price": order_price,
    "isAutomated": "true"
}
response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
print(response.json())
