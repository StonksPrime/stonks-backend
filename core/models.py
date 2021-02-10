from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class Broker(models.Model):
    name = models.CharField(max_length=60)
    country = CountryField()
    fiscal_country = CountryField()
    #interface = models.CharField(max_length=60)
    class Meta:
        db_table = 'broker' #TODO: add core_ in db_table
    
    def __str__(self):
        return "Broker name: %s , country: %s" % (self.name, self.country)

class Investor(AbstractUser):
    country = CountryField(blank=True)
    public_profile = models.BooleanField(default=0)
    birth_date = models.DateField(null=True, blank=True)
    brokers = models.ManyToManyField(Broker, through='Account')
    #profile_picture = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = 'core_investor'

    def __str__(self):
        return "Investor: %s %s" % (self.first_name, self.last_name)

class Account(models.Model):
    person = models.ForeignKey(Investor, null=True, on_delete=models.SET_NULL)
    broker_exchange = models.ForeignKey(Broker, null=True, on_delete=models.SET_NULL)
    broker_username = models.CharField(max_length=60, blank=True)
    broker_password = models.CharField(max_length=60, blank=True)
    token_key = models.CharField(max_length=200, blank=True)
    token_secret = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'core_investor_broker_account'

    def __str__(self):
        return " %s %s's account at: %s" % (self.person.first_name, self.person.last_name, self.broker_exchange.name)

#Not sure if we need this
#class DailyAssetPrice(models.Model):
#    date = models.Date
#    opening_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
#    closing_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
#    minimum_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
#    maximum_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)

class Asset(models.Model):
    name = models.CharField(max_length=60)
    ticker = models.CharField(max_length=60, unique=True)
    sector = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    last_price = models.DecimalField(default=0, max_digits=20, decimal_places=10)

    class Meta:
        db_table = 'core_financial_asset'

    def __str__(self):
        return "%s asset" % (self.ticker)

class Stock(Asset):
    isin = models.CharField(max_length=60)
    country = CountryField()
    region = models.CharField(max_length=60)

    class Meta:
        db_table = 'core_asset_stock'

    def __str__(self):
        return "Stock asset: %s , last price: %d" % (self.name, self.last_price)

class Fiat(Asset):
    country = CountryField()

    class Meta:
        db_table = 'core_asset_fiat'

    def __str__(self):
        return "Fiat asset: %s , %s" % (self.name, self.ticker)

class Fund(Asset):
    isin = models.CharField(max_length=60)
    country = CountryField()
    region = models.CharField(max_length=60)

    class Meta:
        db_table = 'core_asset_fund'

    def __str__(self):
        return "Fund asset: %s , last price: %d" % (self.name, self.last_price)

class ETF(Asset):
    isin = models.CharField(max_length=60)
    country = CountryField()
    region = models.CharField(max_length=60)

    class Meta:
        db_table = 'core_asset_etf'

    def __str__(self):
        return "ETF asset: %s , last price: %d" % (self.name, self.last_price)

class Crypto(Asset):
    
    class Meta:
        db_table = 'core_asset_crypto'

    def __str__(self):
        return "Crypto asset: %s , last price: %d" % (self.ticker, self.last_price)

class Position(models.Model):
    STATUS = (
        ('O', 'Open'),
        ('C', 'Closed'),
        ('P', 'Pending'),
        ('X', 'Canceled'),
    )
    quantity = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    break_even_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    closing_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    opening_date = models.DateTimeField(null=True, editable=True, default=None)
    closing_date = models.DateTimeField(null=True, editable=True, default=None)
    order_status = models.CharField(max_length=1, choices=STATUS)

    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="position_investor")
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING, null=True, related_name="position_asset")
    broker = models.ForeignKey(Broker, on_delete=models.DO_NOTHING, null=True, related_name="position_broker")

    class Meta:
        db_table = 'core_investor_asset_position'

    def __str__(self):
        return "%s %s's %s Position, quantity: %f at %s" % (self.user.first_name, self.user.last_name, self.asset.ticker ,self.quantity, self.broker.name)

#I think this will be on code
#class BrokerInterface(models.Model):
#    name = models.CharField(max_length=60)
#    path = models.CharField(max_length=60)
#    version = models.CharField(max_length=60)
#    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True)

#    def __str__(self):
#        return "Broker %s interface: %s , version: %s" % (self.broker.name, self.name, self.version)