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


config = configparser.ConfigParser()
config.read('./config.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']
app = Flask(__name__)
client = oandapyV20.API(access_token=access_token)

#### TOS

# Create a new session, credentials path is required.
TDSession = TDClient(
    client_id='FQOUAWD87DXUILUXYQI1XIVY3J8OGUPX',
    redirect_uri='https://localhost',
    credentials_path='config.json'
)

# Login to the session
TDSession.login()

#####


format = ''


r = positions.PositionList(accountID=accountID)

def re(integ):
    if len(list(integ)) == 1: return '0'+str(integ)
    else: return str(integ)

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def ONADA_FOREX_CLOSE_POSITIONS():
    r = positions.OpenPositions(accountID=accountID)
    client.request(r)
    data_long = {
        "longUnits": "ALL"
    }

    data_short = {
        "shortUnits": "ALL"
    }
    # r = positions.PositionClose(accountID=accountID,instrument='EUR_USD',data=data_long)
    # r = positions.PositionClose(accountID=accountID,instrument='EUR_USD',data=data_short)

    if not int(client.request(r)['positions'][0]['long']['units']) == 0:
        rv = positions.PositionClose(accountID=accountID, instrument='EUR_USD', data=data_long)
    elif not client.request(r)['positions'][0]['short']['units'] == 0:
        rv = positions.PositionClose(accountID=accountID, instrument='EUR_USD', data=data_short)
    else:
        rv = 'no orders executed'
    print(rv.data)
    return rv.data


def ONADA_FOREX_ORDER(ticker, order_type, qty, price, position_type, exchange):
    print(str(ticker))
    if 'BUY_TO_OPEN' in str(order_type):
        data = {
            "order": {
                "instrument": str(ticker),
                "units": 1000,
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        r = orders.OrderCreate(accountID, data=data)
        client.request(r)
    elif 'SELL_TO_OPEN' in str(order_type):
        data = {
            "order": {
                "instrument": str(ticker),
                "units": -1000,
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        r = orders.OrderCreate(accountID, data=data)
        client.request(r)
    elif 'SELL_TO_CLOSE' in str(order_type):
        print("SELL_TO_CLOSE")
        ONADA_FOREX_CLOSE_POSITIONS()
    elif 'BUY_TO_CLOSE' in str(order_type):
        print("BUY_TO_CLOSE")
        ONADA_FOREX_CLOSE_POSITIONS()


def ALPACA_CRYPTO_ORDER(ticker, order_type, qty, price, position_type, exchange):
    print('not implemented ALPACA order')
    print(ticker, order_type, qty, price, position_type, exchange)


def TOS_SPX_ORDER(ticker, order_type, qty, price, position_type, exchange):
    global format

    print(ticker, order_type, qty, price, position_type, exchange)

    if order_type == "BUY_TO_OPEN":
        format = 'SPXW_' + re(str(date.today().month)) + re(str(date.today().day)) + str(date.today().strftime("%y")) + 'C' + str(
            round(float(price)))
        print(format)
        quote = TDSession.get_quotes(instruments=[format])
        print(format, 'CALL', quote)
    elif order_type == "SELL_TO_OPEN":
        format = 'SPXW_' + re(str(date.today().month)) + re(str(date.today().day)) + str(date.today().strftime("%y")) + 'P' + str(
        round(float(price)))
        print(format)
        quote = TDSession.get_quotes(instruments=[format])
        print(format, 'PUT', quote)
    elif order_type == "SELL_TO_CLOSE":
        print("SELLSELL_TO_CLOSE")
        quote = TDSession.get_quotes(instruments=[format])
        print(format, 'PUT', quote)
    elif order_type == "BUY_TO_CLOSE":
        print("BUYBUY_TO_CLOSE")
        quote = TDSession.get_quotes(instruments=[format])
        print(format, 'PUT', quote)

def TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type, exchange):
    print('not implemented TOS order')
    print(ticker, order_type, qty, price, position_type, exchange)


    # if not client.request(r)['positions'] == []:  # if not empty
    #     print(client.request(r)['positions'])
    #     print(ticker, order_type, qty, price, position_type, exchange)


##################################
# WebHook code
##################################
#   ETHUSD, SELL_TO_OPEN, 1312.8700000000001, 1. - 1.{{ALPACA}}


def parse_webhook_message(webhook_message):
    parsed = str(str(webhook_message))
    ticker = parsed.split(',')[0].replace(' ', '')
    ticker = ticker.replace('b\'', '')
    order_type = parsed.split(',')[1].replace(' ', '')
    price = parsed.split(',')[2].replace(' ', '')
    qty = parsed.split(',')[3].replace(' ', '')
    position_type = parsed.split(',')[4].replace(' ', '')
    exchange = parsed.split(',')[5].replace(' ', '')
    exchange = exchange.replace('{', '')
    exchange = exchange.replace('}', '')
    exchange = exchange.replace('\'', '')
    #print(ticker, order_type, qty, price, position_type, exchange)


    if 'ALPACA' in str(webhook_message).upper():
        print('ALPACA')
        ALPACA_CRYPTO_ORDER(ticker, order_type, qty, price, position_type, exchange)
    elif 'ONADA' in str(webhook_message).upper():
        print('ONADA')
        ONADA_FOREX_ORDER(ticker, order_type, qty, price, position_type, exchange)
    elif 'TOS' in str(webhook_message).upper():
        print('TOS')
        data = TOS_SPX_ORDER(ticker, order_type, qty, round_up(price,-1), position_type, exchange)
        print(data)
    elif 'TRADOVATE' in str(webhook_message).upper():
        print('TRADOVATE')
        TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type, exchange)


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        webhook_message = json.loads(request.data)
    except:
        webhook_message = request.data
    #print(webhook_message)
    parse_webhook_message(webhook_message)
    #   FOREX_ORDER(webhook_message)

    #    if ('EURUSD' in str(webhook_message).upper()):
    #        if ('SELL' in str(webhook_message).upper()):
    #            data = {
    #                "order": {
    #                    "instrument": "EUR_USD",
    #                    "units": "-1000",
    #                    "type": "MARKET",
    #                    "positionFill": "DEFAULT"
    #                }
    #            }
    #            r = orders.OrderCreate(accountID, data=data)
    #            client.request(r)
    # #           create_order = pd.Series(r.response['orderCreateTransaction'])
    #            #print(create_order)
    #        else:
    #            data = {
    #                "order": {
    #                    "instrument": "EUR_USD",
    #                    "units": "1000",
    #                    "type": "MARKET",
    #                    "positionFill": "DEFAULT"
    #                }
    #            }
    #            r = orders.OrderCreate(accountID, data=data)
    #            client.request(r)
    #           create_order = pd.Series(r.response['orderCreateTransaction'])
    # print(create_order)
    return webhook_message


@app.route("/logs", methods=["GET"])
def get_logs():
    return 'ok'


app.run(host='0.0.0.0', port=(int(os.environ['PORT'])))
##################################
# WebHook code
##################################
