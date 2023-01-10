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
                                    params={'symbols': "SPXW230110C03910000", 'greeks': 'false'},
                                    headers={'Authorization': 'Bearer Rt4q8G8ZDWnLafqj2D5r1wT3p5E2',
                                             'Accept': 'application/json'}
                                    )
json_response = response.json()
print(response.status_code)
print(json_response)
print(json_response['quotes']['quote']['last'])