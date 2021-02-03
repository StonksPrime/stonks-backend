import json


class BrokerObject:

    def __init__(self, name, country, fiscal_country):
        self.name = name
        self.country = country
        self.fiscal_country = fiscal_country

    # init

    def getAsJSON(self):
        json.dumps(self.__dict__)

    # getAsJSON

# BrokerObject
