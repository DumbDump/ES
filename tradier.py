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



response = requests.get('https://api.tradier.com/v1/markets/quotes',
                                    params={'symbols': "META", 'greeks': 'false'},
                                    headers={'Authorization': 'Bearer Rt4q8G8ZDWnLafqj2D5r1wT3p5E2',
                                             'Accept': 'application/json'}
                                    )
json_response = response.json()
print(response.status_code)
print(json_response)
print(json_response['quotes']['quote']['last'])
sell_price = 1
format = 'SPXW230117P04000000'

response = requests.post('https://api.tradier.com/v1/accounts/6YA28014/orders',
                         data={'class': 'equity',
                               'symbol': 'META',
                               'side': 'buy',
                               'quantity': '100',
                               'type': 'market',
                               'duration': 'day',
                               'tag': 'my-tag-example-1'},
                         headers={'Authorization': 'Bearer Rt4q8G8ZDWnLafqj2D5r1wT3p5E2',
                                  'Accept': 'application/json'}
                         )

#json_response = response.json()
print(response.status_code)
print(response.text)
