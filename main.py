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
import time
import datetime
from pytz import timezone
#from Tradovate_libs import *
#from Tradovate_libs import liquidate_positions, open_long, open_short, close_long, close_short

DEBUG = 0



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
    #print("LIQUIDATE EXISTING POSITION")
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
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
    #print("All Positins", response.json())
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
    response = requests.post("https://" + API + '/order/liquidateposition', headers=headers, data=body)
    time.sleep(1)



def open_order(ACCESS_TOKEN, account_name, account_number, ticker, Qty,Order_Type):
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
    body = {
        "accountSpec": account_name,
        "accountId": account_number,
        "action": Order_Type,
        "symbol": ticker,
        "orderQty": Qty,
        "orderType": "Market",
        "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
    if DEBUG:
        print("Open Long ", response.json())

def open_order_trailing_stop(ACCESS_TOKEN, account_name, account_number, ticker, Qty,Order_Type, TrailingStop):
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
    body = {
        "accountSpec": account_name,
        "accountId": account_number,
        "action": Order_Type,
        "symbol": ticker,
        "orderQty": Qty,
        "orderType": "Market",
        "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
    OrderID = response.json()['orderId']

    body = {
        "masterid": int(OrderID)
    }

    response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
    price = response.json()[0]['price']
    if Order_Type == "Sell":
        limit_price = price + TrailingStop
        new_order_type = "Buy"
    else:
        limit_price = price - TrailingStop
        new_order_type = "Sell"

    body = {
            "accountSpec": account_name,
            "accountId": account_number,
            "action": new_order_type,
            "symbol": ticker,
            "orderQty": Qty,
            "orderType": "TrailingStop",
            "isAutomated": "true",
            "trailingStop": "true",
            "stopPrice": limit_price
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)

def open_order_limit_profit(ACCESS_TOKEN, account_name, account_number, ticker, Qty,Order_Type, TrailingStop):
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }
    body = {
        "accountSpec": account_name,
        "accountId": account_number,
        "action": Order_Type,
        "symbol": ticker,
        "orderQty": Qty,
        "orderType": "Market",
        "isAutomated": "true"
    }
    response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
    OrderID = response.json()['orderId']
    print("0:",response.json())

    body = {
        "masterid": int(OrderID)
    }

    response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
    price = response.json()[0]['price']
    print("1:",response.json())
    if Order_Type == "Sell":
        limit_price = price - TrailingStop
        new_order_type = "Buy"
    else:
        limit_price = price + TrailingStop
        new_order_type = "Sell"

    body = {
            "accountSpec": account_name,
            "accountId": account_number,
            "action": new_order_type,
            "symbol": ticker,
            "orderQty": Qty,
            "orderType": "Limit",
            "price": limit_price
    }
    #response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
    #print(response.json(),price, limit_price)

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
    global format1
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
    price = round_up(10 * (quote['SPY']['lastPrice']),-1)

    if order_type == "BUY_TO_OPEN":
            format = 'SPXW_' + re(str(date.today().month)) + re(str(date.today().day)) + str(date.today().strftime("%y")) + 'C' + str(
                round(price))
            format1 = 'SPXW_' + re(str(date.today().month)) + re(str(date.today().day)) + str(date.today().strftime("%y")) + 'C' + str(
                round(price+20))
            print(format,format1)
            quote = TDSession.get_quotes(instruments=[format])
            quote1 = TDSession.get_quotes(instruments=[format1])
            leg1 = quote[format]['askPrice']
            leg2 = quote1[format1]['bidPrice']
            spread = leg1-leg2
            print("Buy CALL Spread",format,format1, spread)
            if DEBUG:
                print("Buy Call option", "CALL", format,"Ask Price:", quote[format]['askPrice'])
                print("Buy Call option", "CALL", format, "Ask Price:", quote[format1]['bidPrice'])

    elif order_type == "SELL_TO_OPEN":
            format = 'SPXW_' + re(str(date.today().month)) + re(str(date.today().day)) + str(date.today().strftime("%y")) + 'P' + str(
            round(price))
            format1 = 'SPXW_' + re(str(date.today().month)) + re(str(date.today().day)) + str(date.today().strftime("%y")) + 'P' + str(
            round(price-10))
            quote = TDSession.get_quotes(instruments=[format])
            quote1 = TDSession.get_quotes(instruments=[format1])
            leg1 = quote[format]['askPrice']
            leg2 = quote1[format1]['bidPrice']
            spread = leg1-leg2
            print("Buy to Open PUT Spread",format,format1, spread)
    elif order_type == "SELL_TO_CLOSE":
            quote = TDSession.get_quotes(instruments=[format])
            quote1 = TDSession.get_quotes(instruments=[format1])
            leg1 = quote[format]['askPrice']
            leg2 = quote1[format1]['bidPrice']
            spread = leg1 - leg2
            print("Sell to close CALL Spread", format, format1, spread)
    elif order_type == "BUY_TO_CLOSE":
            quote = TDSession.get_quotes(instruments=[format])
            quote1 = TDSession.get_quotes(instruments=[format1])
            leg1 = quote[format]['askPrice']
            leg2 = quote1[format1]['bidPrice']
            spread = leg1 - leg2
            print("Sell to close PUT Spread", format, format1, spread)

def TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type, exchange):
    if DEBUG:
        print('TRADOVATE order')
        print(ticker, order_type, qty, round(price), position_type, exchange)
        print(ticker, ticker)
    account_number = "1083577"
    account_name = "DEMO485096"
    Qty = 1
    # get token
    headers = {
        "name": "vvnsreddy",
        "password": "Intel123$",
        "appId": "Sample App",
        "appVersion": "1.0",
        "cid": '1133',
        "sec": '66e4c947-0fe2-46b2-b76a-3ed88601ccd8'
    }

    now = datetime.datetime.now()
    today5am = now.replace(hour=6+7, minute=0, second=0, microsecond=0)
    today1pm = now.replace(hour=13+7, minute=0, second=0, microsecond=0)

    if now > today5am and now < today1pm:
        daytime = 1
        daytime_multiplier = 4
    else:
        daytime = 0
        daytime_multiplier = 1

    if DEBUG:
        print("DayTime:",daytime)

    response = requests.post("https://" + API + ACCOUNTS_PATH, params=headers)
    ACCESS_TOKEN = response.json()['accessToken']
    #print(ACCESS_TOKEN)
    headers = {
        "Authorization": 'Bearer ' + str(ACCESS_TOKEN)
    }

    if daytime == 1:
        if ticker == "MESZ2":
            profit_target = 20
            TrailingStop  = 10
        elif ticker == "MNQZ2":
            profit_target = 100
            TrailingStop  = 50
        elif ticker == "ESZ2":
            profit_target = 6
            TrailingStop  = 8
        else:
            profit_target = 20
            TrailingStop  = 100
    else:
        if ticker == "MESZ2":
            profit_target = 4
            TrailingStop  = 10
        elif ticker == "MNQZ2":
            profit_target = 10
            TrailingStop  = 60
        elif ticker == "ESZ2":
            profit_target = 2
            TrailingStop  = 4
        else:
            profit_target = 5
            TrailingStop  = 60


    if order_type == "BUY_TO_OPEN":
        liquidate_positions(ACCESS_TOKEN, account_number, ticker)
        Order_Type = "Buy"
        open_order(ACCESS_TOKEN, account_name, account_number, ticker, Qty,Order_Type)
    elif order_type == "SELL_TO_OPEN":
        liquidate_positions(ACCESS_TOKEN, account_number, ticker)
        Order_Type = "Sell"
        open_order(ACCESS_TOKEN, account_name, account_number, ticker, Qty,Order_Type)
    elif order_type == "SELL_TO_CLOSE":
        liquidate_positions(ACCESS_TOKEN, account_number, ticker)
    elif order_type == "BUY_TO_CLOSE":
        liquidate_positions(ACCESS_TOKEN, account_number, ticker)
    elif order_type == "long":
        liquidate_positions(ACCESS_TOKEN, account_number, ticker)
        Order_Type = "Buy"
        Qty  = 1
        #open_order_trailing_stop(ACCESS_TOKEN, account_name, account_number, ticker, Qty, Order_Type, TrailingStop)
        open_order_limit_profit(ACCESS_TOKEN, account_name, account_number, ticker, Qty, Order_Type, profit_target)
    elif order_type == "short":
        liquidate_positions(ACCESS_TOKEN, account_number, ticker)
        Order_Type = "Sell"
        Qty  = 1
        #open_order_trailing_stop(ACCESS_TOKEN, account_name, account_number, ticker, Qty, Order_Type, TrailingStop)
        open_order_limit_profit(ACCESS_TOKEN, account_name, account_number, ticker, Qty, Order_Type, profit_target)
    elif order_type == "flat":
        liquidate_positions(ACCESS_TOKEN, account_number, ticker)
    elif order_type == "RENKO_LONG":
        body = {
            "name": ticker
        }
        # find contract ID
        response = requests.post("https://" + API + '/contract/find', headers=headers, data=body)
        ID = response.json()['id']
        if DEBUG:
            print(response.json())
            rint("LIQUID:", ID)

        # extract all positions
        response = requests.post("https://" + API + '/position/list', headers=headers)
        if DEBUG:
            print(response.json())
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

        response = requests.post("https://" + API + '/order/liquidateposition', headers=headers, data=body)
        time.sleep(1)

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
        if DEBUG:
            print("Open Long ", response.json())
        OrderID =  response.json()['orderId']
        if DEBUG:
            print("ORDER ID",OrderID)
        #STOP LIMIT SELL
        time.sleep(1)
        body = {
            "masterid": int(OrderID)
        }

        response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)
        if DEBUG:
            print("Retrived Order",response.json())

        if daytime == 0:
            if ticker == "MESZ2":
                order_price = (response.json()[0]['price']) + 3
            elif ticker == "ESZ2":
                order_price = (response.json()[0]['price']) + 3
            elif ticker == "NQZ2":
                order_price = (response.json()[0]['price']) + 8
            else:
                order_price = (response.json()[0]['price']) + 8
        else:
            if ticker == "MESZ2":
                order_price = (response.json()[0]['price']) + 12
            elif ticker == "ESZ2":
                order_price = (response.json()[0]['price']) + 12
            elif ticker == "NQZ2":
                order_price = (response.json()[0]['price']) + 50
            else:
                order_price = (response.json()[0]['price']) + 50

        #print("LIMIT Order Price",order_price)

        body = {
            "accountSpec": "DEMO485096",
            "accountId": 1083577,
            "action": "Sell",
            "symbol": ticker,
            "orderQty": 1,
            "orderType": "Limit",
            "price": int(order_price),
            "isAutomated": "true"
        }
        response = requests.post("https://" + API + '/order/placeorder', headers=headers, data=body)
        if DEBUG:
            print("Limit Order Response", response.json())
    elif order_type == "RENKO_SHORT":
        #print("RENKO SHORT", ticker)
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
#        if (netpos):
        response = requests.post("https://" + API + '/order/liquidateposition', headers=headers, data=body)

        #print("Liqdation done", netpos)
        time.sleep(1)
        # Open Short
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
        #print("Open Short", response.json())
        OrderID = response.json()['orderId']
        #print("OrderID",OrderID)
        time.sleep(1)
        #STOP LIMIT SELL
        body = {
            "masterid": int(OrderID)
        }

        response = requests.post("https://" + API + '/fill/deps', headers=headers, data=body)

        if daytime == 0:
            if ticker == "MESZ2":
                order_price = (response.json()[0]['price']) - 3
            else:
                order_price = (response.json()[0]['price']) - 8
        else:
            if ticker == "MESZ2":
                order_price = (response.json()[0]['price']) - 12
            else:
                order_price = (response.json()[0]['price']) - 50

        print("Price",response.json()[0]['price'],int(order_price))

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
        print("order status",response.json())

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
        if DEBUG:
            print('###########  TRADOVATE ################')
        TV_FUTURE_ORDER(ticker, order_type, qty, price, position_type, exchange)


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        webhook_message = json.loads(request.data)
    except:
        webhook_message = request.data
    if DEBUG:
        print(webhook_message)
    parse_webhook_message(webhook_message)



    if DEBUG:
        print("Current Time",now)
    return webhook_message


@app.route("/logs", methods=["GET"])
def get_logs():
    return 'ok'



app.run(host='0.0.0.0', port=(int(os.environ['PORT'])))
##################################
# WebHook code
##################################