import time
import openapi_client
from pprint import pprint
from openapi_client.api import accounting_api
from openapi_client.model.account import Account
from openapi_client.model.cash_balance import CashBalance
from openapi_client.model.cash_balance_log import CashBalanceLog
from openapi_client.model.cash_balance_snapshot import CashBalanceSnapshot
from openapi_client.model.get_cash_balance_snapshot import GetCashBalanceSnapshot
from openapi_client.model.margin_snapshot import MarginSnapshot
from openapi_client.model.trading_permission import TradingPermission
# Defining the host is optional and defaults to https://demo-api-d.tradovate.com/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo-api-d.tradovate.com/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearer_access_token
configuration = openapi_client.Configuration(
    access_token = 'bd888715-7c0e-47fe-9687-f6051cbb37a8'
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accounting_api.AccountingApi(api_client)
    masterid = 1 # int | id of User entity

    try:
        api_response = api_instance.account_dependents(masterid)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling AccountingApi->account_dependents: %s\n" % e)