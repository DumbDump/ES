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

print(client.request(r))

if not client.request(r)['positions'] == []: #if not empty
    print(client.request(r)['positions'])

##################################
# WebHook code
##################################
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        webhook_message = json.loads(request.data)
    except:
        webhook_message = request.data
        
    print(webhook_message)
    
    if ('EURUSD' in str(webhook_message).upper()):
        if ('SELL' in str(webhook_message).upper()):
            pass
        else:
            pass
    return webhook_message


@app.route("/logs", methods=["GET"])
def get_logs():
    return 'ok'

# app.run(host='0.0.0.0', port=(int(os.environ['PORT'])))
##################################
# WebHook code
##################################
