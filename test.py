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
import datetime as dt
import time
import datetime
import threading


global daytime

now = datetime.datetime.now()
today5am = now.replace(hour=5, minute=0, second=0, microsecond=0)
today6am = now.replace(hour=6 + 7, minute=0, second=0, microsecond=0)
today1pm = now.replace(hour=13 + 7, minute=0, second=0, microsecond=0)

if (now > today6am and now < today1pm):
    print("Current Time", now)
else:
    print("Current Time-----", now)

if now > today5am:
    print("Current Time:", now)

X = "XX"

command = "PLACE;"+X+";"

print(command)