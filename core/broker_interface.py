import abc


class BrokerInterface(abc.ABC):
    @abc.abstractmethod
    def loadInvestorAccount(self, investor):
        pass
    #login

    @abc.abstractmethod
    def updateCurrentPositions(self):
        pass
    #getCurrentPositions

    @abc.abstractmethod
    def getAssetPrice(self, isin, ticker):
        pass
    #getAsset
