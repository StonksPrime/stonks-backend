import degiroapi
import switch as switch
from degiroapi.product import Product

from broker_interface import BrokerInterface
from broker_object import BrokerObject
from asset_object import AssetObject


class DegiroAPI(BrokerInterface):

    def __init__(self):
        super().__init__()
        self.degiroClient = degiroapi.DeGiro()
        self.broker = BrokerObject(BrokerInterface.BrokerTypes.DEGIRO, "NL", "NL")

    # init

    def getBroker(self) -> BrokerObject:
        return self.broker

    # getBroker

    def generateAsset(self, data) -> AssetObject:
        print(data["id"], data["name"], data["currency"], data["closePrice"])

        assetType = data["type"]
        asset = None
        if assetType == "ACC":
            asset = AssetObject(data["name"], AssetObject.AssetTypes.STOCK, data["ticker"], data["sector"],
                                data["description"], data["closePrice"])
            asset.setSTOCKInfo(data["isin"], data["country"], data["region"])
        # STOCK
        return asset

    # generateAsset

    def loadInvestorAccount(self, username, password, token):
        self.degiroClient.login(username, password)
        return

    # loadInvestorAccount

    def geturrentPositions(self) -> list():
        assetsList = list()

        portfolio = self.degiroClient.getdata(degiroapi.Data.Type.PORTFOLIO, True)
        for data in portfolio:
            print(data)

            assetsList.append(self.generateAsset(data))
        return assetsList

    # getCurrentPositions

    def getAssetByISIN(self, isin):
        products = self.degiroClient.search_products(isin)
        productId = Product(products[0]).id

        data = self.degiroClient.product_info(productId)
        print(data["id"], data["name"], data["currency"], data["closePrice"])

        return self.generateAsset(data)

    # getAsset
# degiro
