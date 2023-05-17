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



OrderID = 4926226068



# STOP LIMIT SELL
body = {
    "masterid": OrderID
}
# ticker = "MESZ2"
# response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
# # print(response.json())
# if ticker == "MESZ2":
#     order_price = (response.json()[0]['price']) + 20
# else:
#     order_price = (response.json()[0]['price']) + 40
# print(response.json()[0]['price'], order_price)
# print(int(order_price))
#
# body = {
#     "accountSpec": "DEMO485096",
#     "accountId": 1083577,
#     "action": "Sell",
#     "symbol": ticker,
#     "orderQty": 1,
#     "orderType": "Limit",
#     "price": order_price,
#     "isAutomated": "true"
# }
# response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
# print(response.json())
ticker = "MESZ2"

buy_body = {
    "accountSpec": "DEMO485096",
    "accountId": 1083577,
    "action": "Buy",
    "symbol": ticker,
    "orderQty": 1,
    "orderType": "Market",
}

sell_body = {
    "accountSpec": "DEMO485096",
    "accountId": 1083577,
    "action": "Sell",
    "symbol": ticker,
    "orderQty": 1,
    "orderType": "TrailingStop",
    "isAutomated": "true",
    "trailingStop": "true",
    "stopPrice" : 3884
}

sell_body = {
    "accountSpec": "DEMO485096",
    "accountId": 1083577,
    "action": "Sell",
    "symbol": ticker,
    "orderQty": 1,
    "orderType": "TrailingStop",
    "stopPrice": 20,
    "trailingStop": "true",
    "isAutomated": "true"
}


#response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=buy_body )
#print("Open Long ", response.json())
#OrderID = response.json()['orderId']
#print("ORDER ID", OrderID)
body = {
        "masterid": int(OrderID)
    }

#response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
#price = response.json()[0]['price']
#print("Price", price)

# Order_Type = "Buy"
# TrailingStop = 6
# Qty = 1
#
# if Order_Type == "Sell":
#     limit_price = price + TrailingStop
#     new_order_type = "Buy"
# else:
#     limit_price = price - TrailingStop
#     new_order_type = "Sell"
#
# body = {
#     "accountSpec": "DEMO485096",
#     "accountId": 1083577,
#     "action": new_order_type,
#     "symbol": ticker,
#     "orderQty": Qty,
#     "orderType": "TrailingStop",
#     "isAutomated": "true",
#     "trailingStop": "true",
#     "stopPrice": limit_price
# }
#response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
#print("Open Long ", response.json())

# STOP LIMIT SELL

# body = {
#     "masterid": int(OrderID)
# }
#
# response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
# print("Retrived Order", response.json())
# price = response.json()[0]['price']
# print("price Order", price, price -4)


### Bracket order



# body = {
#     "accountSpec": "DEMO485096",
#     "accountId": 1083577,
#     "action": "sell",
#     "symbol": "ESZ2022",
#     "orderStrategyTypeId": 2,
#     "isAutomated": "true",
#     "params": "{ \"entryVersion\": { \"orderQty\"  : 1, \"orderType\" : \"Market\", \"timeInForce\": \"Day\" }, \"brackets\": [ { \"qty\": 1, \"profitTarget\": 125, \"stopLoss\": -60, \"trailingStop\": true }] }"
# }

# Buy


# buy_body = {
#     "accountSpec": "DEMO485096",
#     "accountId": 1083577,
#     "action": "Buy",
#     "symbol": "MESZ2",
#     "orderQty": 1,
#     "orderType": "Market",
#     "isAutomated": "true"
# }

#response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=buy_body)
#print("buy:", response.json())


body = {
    "accountSpec": "DEMO485096",
    "accountId": 1083577,
    "action": "sell",
    "symbol": "MESH3",
    "orderStrategyTypeId": 2,
    "isAutomated": "true",
    "params": "{ \"entryVersion\": { \"orderQty\"  : 1, \"orderType\" : \"Market\", \"timeInForce\": \"Day\" }, \"brackets\": [ { \"qty\": 1, \"profitTarget\": 125, \"stopLoss\": -60, \"trailingStop\": true }] }"
}
#response = requests.post("https://" + API + '/order/startorderstrategy', headers=headers, data=body)
#print("Open Long ", response.json())

params = {
    "entryVersion": {
        "orderQty": 1,
        "orderType": 'Market'
    },
    "brackets": [{
        "qty": 1,
        "profitTarget": 30,
        "stopLoss": 15,
        "trailingStop": 'false'
    }]
}

body1 = {
    "accountSpec": "DEMO485096",
    "accountId": 1083577,
    "symbol": 'MESZ2',
    "action": 'Sell',
    "orderStrategyTypeId": 2,
    "params" : json.dumps(params)
}

other = {
        "action": "Sell",
        "orderType": "Limit",
        "price": 3635
}

oco = {
            "accountSpec": "DEMO485096",
            "accountId": 1083577,
            "action": "Sell",
            "symbol": "MESH3",
            "orderQty": 1,
            "orderType": "TrailingStop",
            "price": 3590,
            "stopPrice": 3595,
            "isAutomated": "true",
            "other": json.dumps(str(other))
}

# OCO order

inpiut = "https://" + API + '/order/placeoco'
#print(inpiut)

#response = requests.post(inpiut, headers=headers, data=oco)

print("Open Long ", response.text)



