import abc
from enum import Enum


class BrokerInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    # init

    @abc.abstractmethod
    def loadInvestorAccount(self, username, password, token):
        pass

    # loadInvestorAccount

    @abc.abstractmethod
    def updateCurrentPositions(self):
        pass

    # geturrentPositions

    class BrokerTypes(Enum):
        DEGIRO = "Degiro"
        TRADING212 = "T212"
        KRAKEN = "Kraken"
    # BrokerTypes
# BrokerInterface
