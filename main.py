import pandas as pd
import configparser
import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions

from flask import Flask, request, jsonify, render_template, Response
import os, json, requests
import numpy as np
import pandas as pd


config = configparser.ConfigParser()
config.read('./config.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']
app = Flask(__name__)
client = oandapyV20.API(access_token=access_token)

r = positions.PositionList(accountID=accountID)


def ONADA_FOREX_CLOSE_POSITIONS():
    r = positions.OpenPositions(accountID=accountID)
    data_long = {
        "longUnits": "ALL"
    }
    data_short = {
        "shortUnits": "ALL"
    }
    # r = positions.PositionClose(accountID=accountID,instrument='EUR_USD',data=data_long)
    # r = positions.PositionClose(accountID=accountID,instrument='EUR_USD',data=data_short)

    if not int(client.request(r)['positions'][0]['long']['units']) == 0:
        r = positions.PositionClose(accountID=accountID, instrument='EUR_USD', data=data_long)
    elif not client.request(r)['positions'][0]['short']['units'] == 0:
        r = positions.PositionClose(accountID=accountID, instrument='EUR_USD', data=data_short)
    else:
        r = 'no orders executed'

    print(r.data)


def ONADA_FOREX_ORDER(ticker, order_type, qty, price, position_type):
        if 'BUY_TO_OPEN' in str(order_type):
            data = {
                "order": {
                    "instrument": "ticker",
                    "units": "qty",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
            r = orders.OrderCreate(accountID, data=data)
            client.request(r)
        elif 'SELL_TO_OPEN' in str(order_type:
            data = {
                "order": {
                    "instrument": "ticker",
                    "units": "-qty",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
            r = orders.OrderCreate(accountID, data=data)
            client.request(r)
        elif 'SELL_TO_CLOSE' in str(order_type:
            print ("SELL_TO_CLOSE")
            ONADA_FOREX_CLOSE_POSITIONS()
        elif 'BUY_TO_CLOSE' in str(order_type:
            print("BUY_TO_CLOSE")
            ONADA_FOREX_CLOSE_POSITIONS()

def ALPACA_CRYPTO_ORDER(ticker, order_type, qty, price, position_type):
    print('not implemented ALPACA order')

TOS_SPX_ORDER(ticker, order_type, qty, price, position_type):
    print('not implemented TOS order')

TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type):
    print('not implemented TOS order')

if not client.request(r)['positions'] == []: #if not empty
    print(client.request(r)['positions'])


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
    print(ticker, order_type, qty, price, position_type, exchange)
    print(ticker, order_type, qty, price, position_type, exchange)

    if 'ALPACA' on str(webhook_message).upper()):
        print('ALPACA')
        ALPACA_CRYPTO_ORDER(ticker, order_type, qty, price, position_type)
    elif 'ONADA' on str(webhook_message).upper()):
        print('ONADA')
        ONADA_FOREX_ORDER(ticker, order_type, qty, price, position_type)
    elif 'TOS' on str(webhook_message).upper()):
        print('TOS')
        TOS_SPX_ORDER(ticker, order_type, qty, price, position_type)
    elif 'TRADOVATE' on str(webhook_message).upper()):
        print('TRADOVATE') \
        TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type)

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        webhook_message = json.loads(request.data)
    except:
        webhook_message = request.data
    print(webhook_message)
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
            #print(create_order)
    return webhook_message



@app.route("/logs", methods=["GET"])
def get_logs():
    return 'ok'

app.run(host='0.0.0.0', port=(int(os.environ['PORT'])))
##################################
# WebHook code
##################################
