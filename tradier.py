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
import time, pytz
import datetime
from datetime import datetime
from pytz import timezone, utc
from datetime import datetime



# response = requests.get('https://api.tradier.com/v1/markets/quotes',
#                                     params={'symbols': "META", 'greeks': 'false'},
#                                     headers={'Authorization': 'Bearer Rt4q8G8ZDWnLafqj2D5r1wT3p5E2',
#                                              'Accept': 'application/json'}
#                                     )
# json_response = response.json()
# print(response.status_code)
# print(json_response)
# print(json_response['quotes']['quote']['last'])
# sell_price = 1
# format = 'SPXW230117P04000000'




def format_call_spx_option_symbol(price):
    # Get today's date in the format YYYYMMDD
    today_date = datetime.now().strftime('%Y%m%d')

    # Format the price with 8 digits after the decimal point
    formatted_price = "{:.8f}".format(price)

    # Remove decimal point and leading zeros from the price
    formatted_price = formatted_price.replace('.', '').lstrip('0')

    # Combine today's date and formatted price to create the option symbol
    option_symbol = f"SPX{today_date}C{formatted_price}"

    return option_symbol

print(format_call_spx_option_symbol(4995))
SPY140118C00195000
