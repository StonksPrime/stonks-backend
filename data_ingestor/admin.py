from django.contrib import admin
from .models import User, Asset, Stock, Fund, ETF, Crypto, Broker, Position

# Register your models here.
admin.site.register(User)
admin.site.register(Asset)
admin.site.register(Stock)
admin.site.register(Fund)
admin.site.register(ETF)
admin.site.register(Crypto)
admin.site.register(Broker)
admin.site.register(Position)