import abc
from enum import Enum
from broker_object import BrokerObject


class BrokerInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass
    #init

    @abc.abstractmethod
    def getBroker(self) -> BrokerObject:
        pass
    #getBroker

    @abc.abstractmethod
    def loadInvestorAccount(self, username, password, token):
        pass
    #loadInvestorAccount

    @abc.abstractmethod
    def geturrentPositions(self) -> list():
        pass
    #geturrentPositions

    class BrokerTypes(Enum):
        DEGIRO = "Degiro"
        TRADING212 = "T212"
        KRAKEN = "Kraken"
    #BrokerTypes
#BrokerInterface
