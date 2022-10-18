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
        print(response.json())

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
        print(response.json())
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
        print(response.json())
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
        print(response.json())




def parse_webhook_message(webhook_message):
    parsed = str(str(webhook_message))
    ticker = parsed.split(',')[0].replace(' ', '')
    ticker = ticker.replace('b\'', '')
    order_type = parsed.split(',')[1].replace(' ', '')
    price = float(parsed.split(',')[2].replace(' ', ''))
    qty = parsed.split(',')[3].replace(' ', '')
    position_type = parsed.split(',')[4].replace(' ', '')
    exchange = parsed.split(',')[5].replace(' ', '')
    exchange = exchange.replace('{', '')
    exchange = exchange.replace('}', '')
    exchange = exchange.replace('\'', '')
    TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type, exchange)


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        webhook_message = json.loads(request.data)
    except:
        webhook_message = request.data
        parse_webhook_message(webhook_message)



    return webhook_message


@app.route("/logs", methods=["GET"])
def get_logs():
    return 'ok'


app.run(host='0.0.0.0', port=(int(os.environ['PORT'])))
##################################
# WebHook code
##################################
