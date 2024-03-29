from django.contrib import admin
from .models import Broker, Investor, Account, Asset, Stock, Fiat, Fund, ETF, Crypto, Position

# Register your models here.
admin.site.register(Broker)
admin.site.register(Investor)
#admin.site.register(Account)
admin.site.register(Asset)
admin.site.register(Stock)
admin.site.register(Fiat)
admin.site.register(Fund)
admin.site.register(ETF)
admin.site.register(Crypto)
admin.site.register(Position)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("person", "broker_exchange", "broker_username")
    fields = ("person", "broker_exchange", "broker_username")