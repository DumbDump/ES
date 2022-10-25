

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
#from Tradovate_libs import *
#from Tradovate_libs import liquidate_positions, open_long, open_short, close_long, close_short


config = configparser.ConfigParser()
config.read('./config.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']
app = Flask(__name__)
client = oandapyV20.API(access_token=access_token)

#### TOS
long_flag = 0
short_flag = 0
call_option = ""
put_option = ""
# Create a new session, credentials path is required.
TDSession = TDClient(
    client_id='FQOUAWD87DXUILUXYQI1XIVY3J8OGUPX',
    redirect_uri='https://localhost',
    credentials_path='config.json'
)

# Login to the session
TDSession.login()

#####

################
#Tradovate API

API = 	"demo.tradovateapi.com/v1"
ACCOUNT_ID = "vvnsreddy@gmail.com"
ACCOUNTS_PATH = f"/auth/accessTokenRequest"
# Tradovate
account_number = 1083577

# get token
headers = {
         "name": "vvnsreddy@gmail.com",
         "password": "Intel123$",
         "appId": "Sample App",
         "appVersion": "1.0",
         "cid": '1133',
         "sec": '66e4c947-0fe2-46b2-b76a-3ed88601ccd8'
}

##### TRADOVATE SUB ROUTINES


def liquidate_positions(ACCESS_TOKEN, account_number, ticker):
    # form header
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }



    print("LIQUID:",account_number, ticker )
    body = {
        "name": 'ticker'
    }
    # find contract ID
    response = requests.post("https://" + API + '/contract/find', headers=headers, data=body)
    ID = response.json()['id']
    print(response.json())
    print("LIQUID:", ID)

    # extract all positions
    response = requests.post("https://" + API + '/position/list', headers=headers)
    print(response.json())
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

    print("Liqdation done", netpos)


def open_long(ACCESS_TOKEN, account_name, account_number, ticker, Qty):
    print("open_long_data:", account_name, account_number, ticker, Qty)
    # form header
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
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

def close_long(ACCESS_TOKEN, account_name, account_number, ticker, Qty):
    print("open_long_data:", account_name, account_number, ticker, Qty)
    # form header
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
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

def open_short(ACCESS_TOKEN, account_name, account_number, ticker, Qty):
    print("open_long_data:", account_name, account_number, ticker, Qty)
    # form header
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
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

def close_short(ACCESS_TOKEN, account_name, account_number, ticker, Qty):
    print("open_long_data:", account_name, account_number, ticker, Qty)
    # form header
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
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


######



################

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
    print(client.request(r))
    if client.request(r)['positions']:
        print(client.request(r)['positions'][0]['long']['units'])
    data_long = {
        "longUnits": "ALL"
    }

    data_short = {
        "shortUnits": "ALL"
    }
    # r = positions.PositionClose(accountID=accountID,instrument='EUR_USD',data=data_long)
    # r = positions.PositionClose(accountID=accountID,instrument='EUR_USD',data=data_short)

    if client.request(r)['positions']:
        if int(client.request(r)['positions'][0]['long']['units']) != 0:
            rv = positions.PositionClose(accountID=accountID, instrument='EUR_USD', data=data_long)
        elif int(client.request(r)['positions'][0]['short']['units']) != 0:
            rv = positions.PositionClose(accountID=accountID, instrument='EUR_USD', data=data_short)
        else:
            rv = 'no orders executed'
        client.request(rv)
        print(rv.data)



def ONADA_FOREX_ORDER(ticker, order_type, qty, price, position_type, exchange):
    print(str(ticker))
    if 'BUY_TO_OPEN' in str(order_type):
        data = {
            "order": {
                "instrument": "EUR_USD",
                "units": 1000,
                "type": "LIMIT",
                "price": round(float(price),4),
                "positionFill": "DEFAULT"
            }
        }
        r = orders.OrderCreate(accountID, data=data)
        client.request(r)
    elif 'SELL_TO_OPEN' in str(order_type):
        data = {
            "order": {
                "instrument": "EUR_USD",
                "units": -1000,
                "type": "LIMIT",
                "price": round(float(price),4),
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
    global long_flag
    global short_flag
    global call_option
    global put_option
    # Create a new session, credentials path is required.
    TDSession = TDClient(
        client_id='FQOUAWD87DXUILUXYQI1XIVY3J8OGUPX',
        redirect_uri='https://localhost',
        credentials_path='config.json'
    )
    # Login to the session
    TDSession.login()
    #print(ticker, order_type, qty, price, position_type, exchange)

    quote = TDSession.get_quotes(instruments=["SPY"])
    price = 10 * (quote['SPY']['lastPrice'])

    if order_type == "RENKO_LONG":
        #print("SPX RENKO LONG")
        if short_flag == 1:
            quote = TDSession.get_quotes(instruments=[put_option])
            print("Sell put Option", format, "Bid Price:", quote[format]['bidPrice'])
            short_flag = 0
        else:
            format = 'SPXW_' + re(str(date.today().month)) + re(str(date.today().day)) + str(date.today().strftime("%y")) + 'C' + str(
                round(price))
            #print(format)
            quote = TDSession.get_quotes(instruments=[format])
            #print(quote)
            print("Buy Call option", "CALL", format,"Ask Price:", quote[format]['askPrice'])
            call_option = format
            long_flag   = 1
    elif order_type == "RENKO_SHORT":
        #print("SPX RENKO SHORT")
        if long_flag == 1:
            quote = TDSession.get_quotes(instruments=[call_option])
            print("Sell call Option", format, "Bid Price:", quote[format]['bidPrice'])
            long_flag = 0
        else:
            format = 'SPXW_' + re(str(date.today().month)) + re(str(date.today().day)) + str(date.today().strftime("%y")) + 'P' + str(
            round(price))
            #print(format)
            quote = TDSession.get_quotes(instruments=[format])
            #print(quote)
            print("Buy put option", "PUT", format,"Bid Price:", quote[format]['bidPrice'])
            put_option = format
            short_flag = 1


def TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type, exchange):
    #print('TRADOVATE order')
    print(ticker, order_type, qty, round(price), position_type, exchange)
    #print(ticker, ticker)
    # get token
    headers = {
        "name": "vvnsreddy",
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

    if ticker == "MESZ2":
        profit_target = 4
    elif ticker == "MNQZ2":
        profit_target = 10
    elif ticker == "ESZ2":
        profit_target = 5

    if order_type == "BUY_TO_OPEN":
        open_long(account_name, account_number, ticker, 1)
    elif order_type == "SELL_TO_OPEN":
        open_short(account_name, account_number, ticker, 1)
    elif order_type == "SELL_TO_CLOSE":
        close_long(account_name, account_number, ticker, 1)
    elif order_type == "BUY_TO_CLOSE":
        close_short(account_name, account_number, ticker, 1)
    elif order_type == "RENKO_LONG":
        #print("RENKO LONG")
        body = {
            "name": ticker
        }
        # find contract ID
        response = requests.post("https://" + API + '/contract/find', headers=headers, data=body)
        ID = response.json()['id']
        #print(response.json())
        #rint("LIQUID:", ID)

        # extract all positions
        response = requests.post("https://" + API + '/position/list', headers=headers)
        #print(response.json())
        length = len(response.json())

        if (length >= 1 and response.json()[0]['contractId'] == ID):
            netpos = response.json()[0]['netPos']
        elif (length >= 2 and response.json()[1]['contractId'] == ID):
            netpos = response.json()[1]['netPos']
        elif (length >= 3 and response.json()[2]['contractId'] == ID):
            netpos = response.json()[2]['netPos']
        elif (length >= 4 and response.json()[3]['contractId'] == ID):
            netpos = response.json()[3]['netPos']
        else:
            #print("POSTION not found to do liquidation")
            netpos = 0

        body = {
            "accountId": 1083577,
            "contractId": ID,
            "admin": "false",
        }
        if (netpos):
            response = requests.post("https://" + API + '/order/liquidateposition', headers=headers, data=body)

        #print("Liqdation done", netpos)
        # Open Long
        body = {
            "accountSpec": "DEMO485096",
            "accountId": 1083577,
            "action": "Buy",
            "symbol": ticker,
            "orderQty": 1,
            "orderType": "Market",
            "isAutomated": "true"
        }
        response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
        print("Open Long", response.json())
        OrderID =  response.json()
        #STOP LIMIT SELL
        body = {
            "masterid": OrderID
        }

        response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
        # print(response.json())
        order_price = (response.json()[0]['price']) + 40
        print(order_price)

        body = {
            "accountSpec": "DEMO485096",
            "accountId": 1083577,
            "action": "Sell",
            "symbol": "MNQZ2",
            "orderQty": 1,
            "orderType": "Limit",
            "price": order_price,
            "isAutomated": "true"
        }
        response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
        print(response.json())
    elif order_type == "RENKO_SHORT":
        print("RENKO SHORT", ticker)
        body = {
            "name": ticker
        }
        # find contract ID
        response = requests.post("https://" + API + '/contract/find', headers=headers, data=body)
        ID = response.json()['id']
        #print(response.json())
        #print("LIQUID:", ID)

        # extract all positions
        response = requests.post("https://" + API + '/position/list', headers=headers)
        #print(response.json())
        length = len(response.json())

        if (length >= 1 and response.json()[0]['contractId'] == ID):
            netpos = response.json()[0]['netPos']
        elif (length >= 2 and response.json()[1]['contractId'] == ID):
            netpos = response.json()[1]['netPos']
        elif (length >= 3 and response.json()[2]['contractId'] == ID):
            netpos = response.json()[2]['netPos']
        elif (length >= 4 and response.json()[3]['contractId'] == ID):
            netpos = response.json()[3]['netPos']
        else:
            #print("POSTION not found to do liquidation")
            netpos = 0

        body = {
            "accountId": 1083577,
            "contractId": ID,
            "admin": "false",
        }
        if (netpos):
            response = requests.post("https://" + API + '/order/liquidateposition', headers=headers, data=body)

        #print("Liqdation done", netpos)
        # Open Long
        body = {
            "accountSpec": "DEMO485096",
            "accountId": 1083577,
            "action": "Sell",
            "symbol": ticker,
            "orderQty": 1,
            "orderType": "Market",
            "isAutomated": "true"
        }
        response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
        print("Open Short", response.json())
        OrderID = response.json()

        #STOP LIMIT SELL
        body = {
            "masterid": OrderID
        }

        response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
        # print(response.json())
        order_price = (response.json()[0]['price']) - 40
        print(order_price)

        body = {
            "accountSpec": "DEMO485096",
            "accountId": 1083577,
            "action": "Buy",
            "symbol": "MNQZ2",
            "orderQty": 1,
            "orderType": "Limit",
            "price": order_price,
            "isAutomated": "true"
        }
        response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
        print(response.json())

##################################
# WebHook code
##################################
#   ETHUSD, SELL_TO_OPEN, 1312.8700000000001, 1. - 1.{{ALPACA}}


def parse_webhook_message(webhook_message):
    parsed = str(str(webhook_message))
    ticker_temp = parsed.split(',')[0].replace(' ', '')
    ticker = str(ticker_temp.replace('2022','2')).replace("b'", '').replace("'", '')
    order_type = parsed.split(',')[1].replace(' ', '')
    price = float(parsed.split(',')[2].replace(' ', ''))
    qty = parsed.split(',')[3].replace(' ', '')
    position_type = parsed.split(',')[4].replace(' ', '')
    exchange = parsed.split(',')[5].replace(' ', '')
    exchange = exchange.replace('{', '')
    exchange = exchange.replace('}', '')
    exchange = exchange.replace('\'', '')
    print(ticker, order_type, qty, price, position_type, exchange)
    if 'ALPACA' in str(webhook_message).upper():
        print('###########  ALAPCA ################')
        ALPACA_CRYPTO_ORDER(ticker, order_type, qty, price, position_type, exchange)
    elif 'ONADA' in str(webhook_message).upper():
        print('###########  ONADA ################')
        ONADA_FOREX_ORDER(ticker, order_type, qty, price, position_type, exchange)
    elif 'TOS' in str(webhook_message).upper():
        print('###########  TOS ################')
        data = TOS_SPX_ORDER(ticker, order_type, qty, round_up(price,-1), position_type, exchange)
        #print(data,order_type)
    elif 'TRADOVATE' in str(webhook_message).upper():
        print()
        print()
        print('###########  TRADOVATE ################')
        TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type, exchange)


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
    # print(create_order)
    return webhook_message


@app.route("/logs", methods=["GET"])
def get_logs():
    return 'ok'


app.run(host='0.0.0.0', port=(int(os.environ['PORT'])))
##################################
# WebHook code
##################################