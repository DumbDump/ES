import pandas as pd
import configparser
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.orders as orders

config = configparser.ConfigParser()
config.read('./config.ini')

accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']
api = API(access_token=access_token)
client = oandapyV20.API(access_token=access_token)

# Get rates information
params = {"instruments": "EUR_USD,USD_JPY"}

r = pricing.PricingInfo(accountID=accountID, params=params)

rv = api.request(r)

print(r.response)

prices = pd.DataFrame(r.response['prices'])

print(prices)
data = {
    "order": {
        "instrument": "EUR_USD",
        "units": "-100",
        "type": "MARKET",
        "positionFill": "DEFAULT"
    }
}
r = orders.OrderCreate(accountID, data=data)
client.request(r)
create_order = pd.Series(r.response['orderCreateTransaction'])
print(create_order)

