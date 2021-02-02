from . import broker_interface

import sys
import platform
import time
import base64
import hashlib
import hmac
import urllib.request
import json

from core.models import Investor, Broker, Position, Account, Asset, Crypto, Fiat

class KrakenAPI(broker_interface.BrokerInterface):
    """ Loads a session for a given user with the broker"""

    def __init__(self):
        """ Create an object with API information."""

        self.api_public = {"Time", "Assets", "AssetPairs", "Ticker", "OHLC", "Depth", "Trades", "Spread"}
        self.api_private = {"Balance", "BalanceEx", "TradeBalance", "OpenOrders", "ClosedOrders", "QueryOrders", "TradesHistory", "QueryTrades", "OpenPositions", "Ledgers", "QueryLedgers", "TradeVolume", "AddExport", "ExportStatus", "RetrieveExport", "RemoveExport", "GetWebSocketsToken"}
        self.api_trading = {"AddOrder", "CancelOrder", "CancelAll"}
        self.api_funding = {"DepositMethods", "DepositAddresses", "DepositStatus", "WithdrawInfo", "Withdraw", "WithdrawStatus", "WithdrawCancel", "WalletTransfer"}

        self.api_domain = "https://api.kraken.com"
        self.api_data = ""

        self.broker, created = Broker.objects.get_or_create(name='Kraken',country='US',fiscal_country='GB')
        return

    def loadInvestorAccount(self, investor_username):
        """ Load user session with broker

        :param investor_username: user 
        :type investor_username: Investor
        :returns: None
        """
        self.investor = Investor.objects.filter(username=investor_username)[0]
        print(self.investor)

        self.account = Account.objects.filter(person=self.investor, broker_exchange__name='Kraken')[0]
        print (self.account)

        return

    def updateCurrentPositions(self):
        """ Updates current user positions and assets with this broker """

        json_assets = self._query('Assets')
        assets = json.loads(json_assets)
        #for asset in assets["result"]:
        #    print ("Asset: " + asset + str(assets["result"][asset]))

        json_balance = self._query('Balance')
        balance = json.loads(json_balance)
        for currency in balance["result"]:
            amount=balance["result"][currency]
            print ("Currency: " + currency + str(amount))
            asset_name = assets["result"][currency]['altname']
            prefix = currency.replace(asset_name,'')

            if (prefix=='Z'):                    # Asset type = fiat money
                asset, created = Fiat.objects.get_or_create(ticker=asset_name)
             
            if (prefix=='X' or prefix==''):     # Asset type = cryptocurrency
                if (asset_name == 'XBT'):           # Fix Kraken weird ticker
                    asset_name = asset_name.replace('XBT','BTC')

                asset, created = Crypto.objects.get_or_create(ticker=asset_name)
            
            Position.objects.update_or_create(asset=asset, user=self.investor, broker=self.broker
                                            , defaults = { 'quantity': amount, 'order_status':'C'})
             
        

    def getAssetPrice(self, isin, ticker):
        return 1



    def _query(self, api_method):
        """ Low-level query handling.

        :param api_method: API request method whether public or private
        :type api_method: str
        :returns: `requests.Response.json`-deserialised Python object
        :raises: `requests.HTTPError`: if response status not successful
        """
        if api_method in self.api_private or api_method in self.api_trading or api_method in self.api_funding:
            self.api_path = "/0/private/"
            api_nonce = str(int(time.time()*1000))

            api_key = self.account.token_key 
            api_secret = base64.b64decode(self.account.token_secret)

            api_postdata = self.api_data + "&nonce=" + api_nonce
            api_postdata = api_postdata.encode('utf-8')
            api_sha256 = hashlib.sha256(api_nonce.encode('utf-8') + api_postdata).digest()
            api_hmacsha512 = hmac.new(api_secret, self.api_path.encode('utf-8') + api_method.encode('utf-8') + api_sha256, hashlib.sha512)
            api_request = urllib.request.Request(self.api_domain + self.api_path + api_method, api_postdata)
            api_request.add_header("API-Key", api_key)
            api_request.add_header("API-Sign", base64.b64encode(api_hmacsha512.digest()))
            api_request.add_header("User-Agent", "Kraken REST API")
        elif api_method in self.api_public:
            self.api_path = "/0/public/"
            api_request = urllib.request.Request(self.api_domain + self.api_path + api_method + '?' + self.api_data)
            api_request.add_header("User-Agent", "Kraken REST API")

        try:
            api_reply = urllib.request.urlopen(api_request).read()
        except Exception as error:
            print("API call failed (%s)" % error)

        try:
            api_reply = api_reply.decode()
        except Exception as error:
            if api_method == 'RetrieveExport':
                sys.stdout.buffer.write(api_reply)
            print("API response invalid (%s)" % error)

        if '"error":[]' in api_reply:
            return api_reply
        else:
            print(api_reply)
            return api_reply

        return api_reply
