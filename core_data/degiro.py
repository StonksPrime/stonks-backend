import degiroapi
from degiroapi.product import Product
#from .models import Position, Broker, Asset
import broker_interface


class DegiroAPI(broker_interface.BrokerInterface):
    degiroClient = degiroapi.DeGiro()

    def login(self, user, password, token):
        self.degiroClient.login(user, password, token)
    #login

    def logout(self):
        self.degiroClient.logout()
    #logout

    def updateCurrentPositions(self):
        portfolio = self.degiroClient.getdata(degiroapi.Data.Type.PORTFOLIO, True)
        for data in portfolio:
            print(data)
    #getCurrentPositions

    def getAssetByISIN(self, isin):
        products = self.degiroClient.search_products(isin)
        productId = Product(products[0]).id

        info = self.degiroClient.product_info(productId)
        print(info["id"], info["name"], info["currency"], info["closePrice"])
    #getAsset