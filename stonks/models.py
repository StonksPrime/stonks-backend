from django.db import models

#TODO: ADD foreign keys
#TODO: print strings

class Position(models.Model):
    STATUS = (
        ('O', 'Open'),
        ('C', 'Closed'),
        ('P', 'Pending'),
        ('X', 'Canceled'),
    )
    name = models.CharField(max_length=60)
    order_status = models.CharField(max_length=1, choices=STATUS)

class Asset(models.Model):
    name = models.CharField(max_length=60)
    ticker = models.CharField(max_length=60)
    sector = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    last_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)

class DailyAssetPrice(models.Model):
    date = models.Date
    opening_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    closing_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    minimum_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    maximum_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)


class Stock(Asset):
    isin = models.CharField(max_length=60)
    country = CountryField()
	region = models.CharField(max_length=60)

	def __str__(self):
        return "Stock asset: %s , last price: %d" % (self.name, self.last_price)

class Fund(Asset):
    isin = models.CharField(max_length=60)
    country = CountryField()
	region = models.CharField(max_length=60)

	def __str__(self):
        return "Fund asset: %s , last price: %d" % (self.name, self.last_price)

class ETF(Asset):
    isin = models.CharField(max_length=60)
    country = CountryField()
	region = models.CharField(max_length=60)

	def __str__(self):
        return "ETF asset: %s , last price: %d" % (self.name, self.last_price)

class Crypto(Asset):

	def __str__(self):
        return "Crypto asset: %s , last price: %d" % (self.name, self.last_price)

class Broker(models.Model):
    name = models.CharField(max_length=60)
    country = CountryField()
    fiscal_country = CountryField()

    def __str__(self):
        return "Broker name: %s , country: %s" % (self.name, self.country)

class BrokerInterface(models.Model):
    name = models.CharField(max_length=60)
    path = models.CharField(max_length=60)
    version = models.CharField(max_length=60)
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Broker %s interface: %s , version: %s" % (self.broker.name, self.name, self.version)