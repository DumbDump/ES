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
import datetime



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

# Function to print symbol and cost_basis
def get_cost_basis_for_symbol(data, target_symbol):
    # Check if the dictionary structure is as expected
    if 'positions' in data and 'position' in data['positions']:
        positions = data['positions']['position']

        # Search for the given symbol in the positions
        for position in positions:
            if 'symbol' in position and 'cost_basis' in position:
                if position['symbol'] == target_symbol:
                    return position['cost_basis']

    # Return None if the symbol is not found
    return None



response = requests.get('https://sandbox.tradier.com/v1/accounts/VA88823939/positions',
                        params={},
                        headers={'Authorization': 'Bearer pOPACO7fKI7Alz4hHIQB66jFDACP', 'Accept': 'application/json'}
                        )
json_response = response.json()
#print(response.status_code)
#print(json_response)
data = json_response

print(data)


#positions = data['positions']


# Check if 'positions' key exists in the data
if 'positions' in data:
    positions = data['positions'].get('position')

    # Check if 'position' key exists and is a list
    if positions and isinstance(positions, list):
        number_of_positions = len(positions)

        # Check if the number of positions is equal to 1
        if number_of_positions == 1:
            # Assign symbol and cost_basis/100 for the first position
            first_position = positions[0]
            symbol = first_position.get('symbol', None)
            cost_basis = first_position.get('cost_basis', None)

            if symbol and cost_basis is not None:
                adjusted_cost_basis = cost_basis / 100

                # Perform tasks with the assigned symbol and adjusted cost_basis
                print(f"Symbol assigned: {symbol}")
                print(f"Adjusted Cost Basis: {adjusted_cost_basis}")
                # Add more tasks if needed
                command = 'do_sell'

            else:
                print("Symbol or Cost Basis not found in the position data.")
                command = no_positions
        else:
            print(f"Number of positions is not equal to 1. It is {number_of_positions}.")
            command = 'flushall'
    else:
        print("Position data is not in the expected format.")
else:
    print("No positions data found.")

print("command:",command)

if command == 'flushall':
        print("flush all command")

if command == 'do_sell':
    print ("do sell")


# target_symbol = 'SPXW240118P04760000'
# cost_basis = get_cost_basis_for_symbol(data, target_symbol)
# cost_basis = data['positions']['position']['cost_basis']
# target_symbol = data['positions']['position']['symbol']
# sell_price1 = (cost_basis/100) + 2
# sell_price = round(sell_price1-2,0)
# print(target_symbol,cost_basis,sell_price)

# cost_basis_list = [position['cost_basis'] for position in data['positions']['position']]
#
# for position in data['positions']['position']:
#     print(f"Cost Basis: {position['cost_basis']}")
#     print(f"Symbol: {position['symbol']}")
#     print()  # Add an empty line between entries if needed
#
# #print(positions['cost_basis'])
# for k, interal_dict in data['positions'].items():
#     print(interal_dict['cost_basis'], interal_dict['symbol'])
#     brought_price = interal_dict['cost_basis']
#     print("purchase price",brought_price)
#     sell_price = brought_price + 2
#     print("sell price",sell_price)


# for position in positions:
#     symbol = position['symbol']
#     quantity = position['quantity']
#     print("Symbol: {}, Quantity: {}".format(symbol, quantity))
#     if quantity < 0:
#         order_type = 'buy_to_cover'
#     else:
#         order_type = 'sell'
#     if not symbol.startswith("SPX"):
#         response = requests.post('https://sandbox.tradier.com/v1/accounts/VA88823939/orders',
#                                  data={'class': 'equity',
#                                        'symbol': symbol,
#                                        'side': order_type,
#                                        'quantity': quantity,
#                                        'type': 'market',
#                                        'duration': 'day',
#                                        'tag': 'my-tag-example-1'},
#                                  headers={'Authorization': 'Bearer pOPACO7fKI7Alz4hHIQB66jFDACP',
#                                           'Accept': 'application/json'}
#                                  )
#         json_response = response.json()
#         print(response.status_code)
#         print(response.text)
# else:
#     print("not stock")
