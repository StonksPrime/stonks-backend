from core.brokers import degiroapi
from core.brokers.degiroapi.product import Product
from core.brokers.broker_interface import BrokerInterface
from core.models import Broker, Investor, Account, Stock, ETF, Position


class DegiroAPI(BrokerInterface):

    def __init__(self):
        super().__init__()
        self.degiroClient = degiroapi.DeGiro()
        self.broker, created = Broker.objects.get_or_create(name='Degiro', country='NL', fiscal_country='NL')
        self.investor = None
        self.account = None
    # init

    def loadInvestorAccount(self, investor_username, username, password, twoWay=""):
        self.degiroClient.login(investor_username, password, twoWay)
        self.investor = Investor.objects.filter(username=username)[0]
        print(self.investor)

        #self.account = Account.objects.filter(person=self.investor, broker_exchange__name='Degiro')[0]
        print(self.account)

        return
    # loadInvestorAccount

    def updateCurrentPositions(self):
        portfolio = self.degiroClient.getdata(degiroapi.Data.Type.PORTFOLIO, True)
        print (portfolio)
        print (' ')
        for data in portfolio:
            if data["positionType"] == "PRODUCT":
                print (data)
                productInfo = self.degiroClient.product_info(data["id"])
                print (productInfo)
                if productInfo["productType"] == "STOCK":
                    asset, created = Stock.objects.get_or_create(name=productInfo["name"], ticker=productInfo["symbol"], last_price= float(data["price"]))
                # Stock
                elif productInfo["productType"] == "ETF":
                    asset, created = ETF.objects.get_or_create(name=productInfo["name"], ticker=productInfo["symbol"], last_price= float(data["price"]))
                #ETF
                #solament guardar els productes
                print (productInfo)
                Position.objects.update_or_create(asset=asset, user=self.investor, broker=self.broker, 
                                                    defaults={'quantity': float(data["size"]), 
                                                    'break_even_price': float(data["breakEvenPrice"]), 'order_status': 'C'})
        #iterar els productes
    # updateCurrentPositions

    def getAssetById(self, id):
        products = self.degiroClient.search_products(id)
        productId = Product(products[0]).id

        data = self.degiroClient.product_info(productId)
        print(data)

        return self.generateAsset(data)
    # getAsset
# degiro
