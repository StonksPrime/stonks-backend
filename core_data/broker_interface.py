import abc


class BrokerInterface(abc.ABC):
    @abc.abstractmethod
    def login(self, user, password):
        pass
    #login

    @abc.abstractmethod
    def logout(self):
        pass
    #logout

    @abc.abstractmethod
    def updateCurrentPositions(self):
        pass
    #getCurrentPositions

    @abc.abstractmethod
    def getAssetByISIN(self, ISIN):
        pass
    #getAsset
