import pandas as pd
import configparser
import oandapyV20
import oandapyV20.endpoints.orders as orders

config = configparser.ConfigParser()
config.read('./config/config.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']

client = oandapyV20.API(access_token=access_token)


# Create an order for an Account
data = {
  "order": {
    "price": "1.2",
    "stopLossOnFill": {
      "timeInForce": "GTC",
      "price": "1.22"
    },
    "timeInForce": "GTC",
    "instrument": "EUR_USD",
    "units": "-100",
    "type": "LIMIT",
    "positionFill": "DEFAULT"
  }
}

# r = orders.OrderCreate(accountID, data=data)
# client.request(r)
# create_order = pd.Series(r.response['orderCreateTransaction'])
# print(create_order)

# Get a List of Orders for an Account
r = orders.OrderList(accountID)
client.request(r)
account_orders_list = pd.Series(r.response['orders'][0])
print(account_orders_list)

# List all Pending Orders in an Account, before you cancel an order (pending order == open order)
# (use OrdersPending(), in lieu of the above OrderList() to cancel open orders)
r = orders.OrdersPending(accountID)
client.request(r)
res = r.response['orders']
last_order_id = res[0]['id'] # also used directly below to get details for a single order
# print(res)

display_all_pending_orders = pd.Series(r.response['orders'][0]) # or pd.Series(res['orders'][0])
print(display_all_pending_orders)

# Get Details for a Single Order in an Account
r = orders.OrderDetails(accountID=accountID, orderID=last_order_id)
client.request(r)
single_order_details = r.response
print(single_order_details)

# Replace an Order in an Account by simultaneously cancelling it and creating a replacement Order.
replacement_order_data = {
  "order": {
    "units": "-500000",
    "instrument": "EUR_USD",
    "price": "1.25000",
    "type": "LIMIT"
  }
}

r = orders.OrderReplace(accountID=accountID, orderID=last_order_id, data=replacement_order_data)
client.request(r)
print(r.response)
req_id = r.response['lastTransactionID'] # store lastTransactionID here because it will be used below for cancellation

# Cancel a pending Order in an Account.
client.request(r)
r = orders.OrderCancel(accountID=accountID, orderID=req_id)
print(r.response)

# Execute A Market Order
market_order_data = {"order":
        {"units": "100",
         "instrument": "GBP_USD",
         "timeInForce": "FOK",
         "type": "MARKET",
         "positionFill": "DEFAULT"
        },
      }

r = orders.OrderCreate(accountID, data=market_order_data)
client.request(r)
print(r.response)

## order confirmation output:
print(r.response)
orderCreateTransaction = pd.Series(r.response['orderCreateTransaction'])
orderFillTransaction = pd.Series(r.response['orderFillTransaction'])
print(orderCreateTransaction)
print(orderFillTransaction)
