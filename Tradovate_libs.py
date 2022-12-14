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
API = 	"demo.tradovateapi.com/v1"


def liquidate_positions(account_number, ticker):
    print("LIQUID:", account_number, ticker);
    body = {
        "name": ticker
    }
    # find contract ID
    response = requests.post("https://" + API + '/contract/find', headers=headers, data=body)
    ID = response.json()['id']

    # extract all positions
    response = requests.post("https://" + API + '/position/list', headers=headers)
    # print(response.json())
    if (response.json()[0]['contractId'] == ID):
        netpos = response.json()[0]['netPos']
    elif (response.json()[1]['contractId'] == ID):
        netpos = response.json()[1]['netPos']
    elif (response.json()[2]['contractId'] == ID):
        netpos = response.json()[2]['netPos']
    elif (response.json()[3]['contractId'] == ID):
        netpos = response.json()[3]['netPos']

    body = {
        "accountId": account_number,
        "contractId": ID,
        "admin": "false",
    }
    if (netpos):
        response = requests.post("https://" + API + '/order/liquidateposition', headers=headers, data=body)
    print("Liqdation done")


def open_long(account_name, account_number, ticker, Qty):
    body = {
        "accountSpec": account_name,
        "accountId": account_number,
        "action": "Buy",
        "symbol": ticker,
        "orderQty": Qty,
        "orderType": "Market",
        "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
    print("Open Long",response.json())

def close_long(account_name, account_number, ticker, Qty):
    body = {
        "accountSpec": account_name,
        "accountId": account_number,
        "action": "Sell",
        "symbol": ticker,
        "orderQty": Qty,
        "orderType": "Market",
        "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
    print("Close Long", response.json())

def open_short(account_name, account_number, ticker, Qty):
    body = {
        "accountSpec": account_name,
        "accountId": account_number,
        "action": "Sell",
        "symbol": ticker,
        "orderQty": Qty,
        "orderType": "Market",
        "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
    print("Open Short", response.json())

def close_short(account_name, account_number, ticker, Qty):
    body = {
        "accountSpec": account_name,
        "accountId": account_number,
        "action": "Buy",
        "symbol": ticker,
        "orderQty": Qty,
        "orderType": "Market",
        "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
    print("Close Short", response.json())

def long_limit_sell_order(account_name, account_number, ticker, Qty, profit_target):
    body = {
            "accountSpec": "DEMO485096",
            "accountId": '1083577',
            "action": "Sell",
            "symbol": ticker,
            "orderQty": Qty,
            "orderType": "Limit",
            "price": executedPrice + profit_target,
            "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)

def short_limit_close_order(account_name, account_number, ticker, Qty, profit_target):
    body = {
            "accountSpec": "DEMO485096",
            "accountId": '1083577',
            "action": "Buy",
            "symbol": ticker,
            "orderQty": Qty,
            "orderType": "Limit",
            "price": executedPrice + profit_target,
            "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)