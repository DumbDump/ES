import pandas as pd
import configparser
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions

config = configparser.ConfigParser()
config.read('./config.ini')

accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']
api = API(access_token=access_token)
client = oandapyV20.API(access_token=access_token)



# r = pricing.PricingInfo(accountID=accountID, params=params)
# rv = api.request(r)
# print(r.response)
# prices = pd.DataFrame(r.response['prices'])

# print(prices)
# data = {
#     "order": {
#         "instrument": "EUR_USD",
#         "units": "-100",
#         "type": "MARKET",
#         "positionFill": "DEFAULT"
#     }
# }
# r = orders.OrderCreate(accountID, data=data)
# client.request(r)
# create_order = pd.Series(r.response['orderCreateTransaction'])
# print(create_order)

r = positions.OpenPositions(accountID=accountID)
client.request(r)
print(client.request(r)['positions'])

data_long = {
        "longUnits": 1000
}
data_short = {
        "shortUnits": 1000
}

#r = positions.PositionClose(accountID=accountID,instrument='EUR_USD',data=data_long)
#r = positions.PositionClose(accountID=accountID,instrument='EUR_USD',data=data_short)

if  client.request(r)['positions']:
        if  int(client.request(r)['positions'][0]['long']['units']) != 0:
                r = positions.PositionClose(accountID=accountID, instrument='EUR_USD', data=data_long)
        elif  client.request(r)['positions'][0]['short']['units'] != 0:
                r = positions.PositionClose(accountID=accountID, instrument='EUR_USD', data=data_short)
        else:
                r = 'no orders executed'

