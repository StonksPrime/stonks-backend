import json
from enum import Enum


class AssetObject:

    def __init__(self, name, type, ticker, sector, description, last_price):
        self.name = name
        self.type = type
        self.ticker = ticker
        self.sector = sector
        self.description = description
        self.last_price = last_price

        self.isin = None
        self.country = None
        self.region = None

    # init

    def setSTOCKInfo(self, isin, country, region):
        self.isin = isin
        self.country = country
        self.region = region

    # setSTOCKInfo

    def setFIATInfo(self, country):
        self.country = country

    # setFIATInfo

    def setFUNDInfo(self, isin, country, region):
        self.isin = isin
        self.country = country
        self.region = region

    # setFUNDInfo

    def setETFInfo(self, isin, country, region):
        self.isin = isin
        self.country = country
        self.region = region

    # setETFInfo

    def setCRYPTOInfo(self, isin, country, region):
        self.isin = isin
        self.country = country
        self.region = region

    # setCRYPTOInfo

    def getAsJSON(self):
        json.dumps(self.__dict__)

    # getAsJSON

    class AssetTypes(Enum):
        STOCK = "Stock"
        FIAT = "Fiat"
        FUND = "Fund"
        ETF = "ETF"
        CRYPTO = "Crypto"
    # AssetTypes
# AssetObject
