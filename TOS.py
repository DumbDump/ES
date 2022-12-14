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


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


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

quote = TDSession.get_quotes(instruments=["SPY"])
print(quote)
price = round_up(10 * quote['SPY']['lastPrice'],-1)
print(price)
#round_up(price,-1)
#print("Ask Price:", quote['SPXW_101322C3670']['askPrice'])

