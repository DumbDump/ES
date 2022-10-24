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
    "name": "vvnsreddy@gmail.com",
    "password": "Intel123$",
    "appId": "Sample App",
    "appVersion": "1.0",
    "cid": '1133',
    "sec": '66e4c947-0fe2-46b2-b76a-3ed88601ccd8'
}

response = requests.post("https://" + API + ACCOUNTS_PATH, params=headers)
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



body = {
    "name": "ESZ2"
}
print("find position ID")
response = requests.post("https://" + API + '/contract/find', headers=headers, data=body)


ID=response.json()['id']
print("ID:", ID)
print(response.json())

response = requests.post("https://" + API + '/position/list', headers=headers)


#print("netpos =",netpos)
#print("Brought Price =", executedPrice)

#print(response.json()[0]['contractId'])
#print(response.json()[1]['contractId'])

body = {
    "id": '4885903810'
}
body = {
    "accountId": '1083577',
    "contractId": '2665264',
    "admin": "false"
}
#print("find position details")
#response = requests.post("https://" + API + '/order/liquidateposition', headers=headers, data=body)
#print(response.json())

# body = {
#     "id": int(2665264)
# }
# response = requests.post("https://" + API + '/position/item', headers=headers, data=body,params=body)
# #netpositions = response.json()[0]['netPos']
# #print(netpositions)
# print(response.json())

body = {
    "accountSpec": "DEMO485096",
    "accountId": '1083577',
    "action": "Buy",
    "symbol": "ESZ2",
    "orderQty": '1',
    "orderType": "Market",
    "isAutomated": "true"
}
#response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
#ID = response.json()
#print(ID)
#print(response.json())
#    "id": '4900472332'
body = {
    "id": ID
}

#response = requests.post("https://" + API + '/executionreport/item', headers=headers, data=body)
#print(response.json())

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#if(current_time < 13:16:00) :
#    print("Hello")

ticker = "MNQZ2"


body = {
    "name": ticker
}
# find contract ID
response = requests.post("https://" + API + '/contract/find', headers=headers, data=body)
ID = response.json()['id']
print(response.json())
# extract all positions
response = requests.post("https://" + API + '/position/list', headers=headers)
print(response.json())



print("LIQUID:", ID)

if (response.json()[0]['contractId'] == ID):
    netpos = response.json()[0]['netPos']
elif (response.json()[1]['contractId'] == ID):
    netpos = response.json()[1]['netPos']
elif (response.json()[2]['contractId'] == ID):
    netpos = response.json()[2]['netPos']
elif (response.json()[3]['contractId'] == ID):
    netpos = response.json()[3]['netPos']