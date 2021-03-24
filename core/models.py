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
    profile_picture = models.CharField(max_length=400, null=True)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
    thumbnail_url = models.URLField(max_length=200, null=True)

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

#========================================= TODO: REVIEW THIS IN THE NEXT MEETING ====================================================
'''
class Watchlist(models.Model):
    #Model to let the user track and group multiple assets. one user CAN HAVE MULTIPLE WATCHLISTS

    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???"") #TODO: Add related name
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name
    name = models.CharField(max_length=60)

    class Meta:
        db_table = 'core_asset_watchlist'

    def __str__(self):
        return "Asset watchlist: %s from user: %d" % (self.name, self.user)


class UserAssetStrategy(models.Model): 
     #Model to track the user strategies for a given assets.

    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc
    name = models.CharField(max_length=60)
    observations = models.CharField(max_length=500)
    in_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    out_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)

    class Meta:
        db_table = 'core_user_asset_strategy'

    def __str__(self):
        return "Asset: %s from user: %d. In price: %s. Out price: %s" % (self.name, self.user, self.in_price, self.out_price)
'''
#========================================= TODO: ALSO DISCUSS THIS IN THE NEXT MEETING (NOTIFICATION AND PATTERN MODELS)==========================
'''
class NotificationType(models.Model):
    #class to define and add new type of notifications into the system. Only by admins

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    
    #TODO: fill table with this values at least
    #asset_price_notifications      -> To notify a changing price of an asset. The user can configure multiple price notifications for one or multiple assets.
    #asset_news_notifications       -> To notify incomming news from an asset. The user must have the "news notification" activated for each asset he wants to receive "news alerts" from.
    #tax_user_notifications         -> Depending on the user's country, the system will remember the user from upcoming tax models he has to fill. The user also can add notifications of this type from his own criteria.
    #balance_user_notifications     -> The user can configure notifications if his entire account balance goes higher or lower than a given value or percentage. The user can also configure it by the type of assets
    #                                  he has in his account (for example, he can add an alert if his entire account reaches 5000€, he can add an alert if his crypto portfolio reaches 2500€ or if his nasdaq portfolio reaches 1200€)
    #watchlist_user_notifications   -> TODO: define better this one. User can add notifications for a given watchlist.
    #asset_pattern_notification     ->  The system can notify the user that a concrete pattern is formed on an asset from his watchlists

class NotificationTypeUserConfig(models.Model):
    #TODO: Model to let the users configure each type of notifications (if the user wants to receive the notification via frontend, email, sms, etc.)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc
    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc
    notify_by_frontend = models.BooleanField()
    notify_by_email = models.BooleanField()
    notify_by_sms = models.BooleanField()
    notifications_activated = models.BooleanField()

class NotificationScheduleConfig(models.Model):
    notification_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc
    seconds_between_executions = models.IntegerField()
    start_execution_datetime = models.DateTimeField()

class Notification(models.Model):
    #TODO: When the notification is triggered ,it's deleted from this table and saved to the pertinent queue, DEPENDING ON THE USER CONFIGURATION
    notification_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc
    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc
    created_by = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc. This field is to know the user who created this alert. It could be
                                                                                                        #created from an investor or from a system module (pattern detection module, tax_scheduled notification, etc. )
                                                                                                        #EACH TYPE OF MODULE HAS IT'S OWN USER IN THE SYSTEM SO WE CAN TRACE FROM WHERE THE NOTIFICATIONES WERE GENERATED
    created_datetime = models.DateTimeField() #datetime when the notification was created into the system

#============Notification queues explanation=========
#The reason to separate the diferent types of notification into different tables is to preserve data integrity in the future if the specific tables requiere new fields or if the specific system thread that processes the 
# queue table encounters a critical problem and stops.
#If something breaks for one type of notification, the others still will be processed without problems.

#For better reability and redundancy I would create separate scripts/projects that read and process each model of notificationQueue

class NotificationFrontendQueue(models.Model):
    #When the user "reads" the notification on the frontend the field "seen_by_user_datetime" is checked, then the register goes to NotificationHistory and is deleted from this table.
    #This type of alert only is shown in the frontend of the app like in a notifications tab or something like this.
    notification_fk_id = ID FROM THE NOTIFICATION TABLE (the notification model holds the primary ID of every notification in the system) #-> this will be filled in the process of inserting the register from the Notifications table
    notification_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc -> this will be filled in the process of inserting the register from the Notifications table
    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc -> this will be filled in the process of inserting the register from the Notifications table
    created_by = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc. -> this will be filled in the process of inserting the register from the Notifications table
    created_datetime = models.DateTimeField() #datetime when the notification was created into the system -> this will be filled in the process of inserting the register from the Notifications table
    triggered_datetime = models.DateTimeField() #datetime when the conditions matched to trigger the notification. This is filled at the time of the INSERTION on this table.
    sent_datetime = models.DateTimeField() #datetime when the schedule lot processes this register.
    seen_datetime = models.DateTimeField() #datetime when the user have seen/clicked the notification on the frontend. When this is filled, the register is DELETED from this table and INSERTED into NotificaitonHistory
    #NOTE: Only FrontendQueue has the seen_datetime.

class NotificationEmailQueue(models.Model):
    #When the notification is inserted into this table, it will be processed in the next scheduled lot, the field "sent_datetime" will be filled, and the registry will be deleted from this table and inserted into NotificationHistory
    notification_fk_id = ID FROM THE NOTIFICATION TABLE (the notification model holds the primary ID of every notification in the system) #-> this will be filled in the process of inserting the register from the Notifications table
    notification_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc -> this will be filled in the process of inserting the register from the Notifications table
    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc -> this will be filled in the process of inserting the register from the Notifications table
    created_by = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc. -> this will be filled in the process of inserting the register from the Notifications table
    created_datetime = models.DateTimeField() #datetime when the notification was created into the system -> this will be filled in the process of inserting the register from the Notifications table
    triggered_datetime = models.DateTimeField() #datetime when the conditions matched to trigger the notification. This is filled at the time of the INSERTION on this table.
    sent_datetime = models.DateTimeField() #datetime when the schedule lot processes this register. When this is filled, the register is DELETED from this table and INSERTED into NotificaitonHistory 

class NotificationsSMSQueue(models.Model):
    #When the notification is inserted into this table, it will be processed in the next scheduled lot, the field "sent_datetime" will be filled, and the registry will be deleted from this table and inserted into NotificationHistory
    notification_fk_id = ID FROM THE NOTIFICATION TABLE (the notification model holds the primary ID of every notification in the system) #-> this will be filled in the process of inserting the register from the Notifications table
    notification_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc -> this will be filled in the process of inserting the register from the Notifications table
    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc -> this will be filled in the process of inserting the register from the Notifications table
    created_by = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc. -> this will be filled in the process of inserting the register from the Notifications table
    created_datetime = models.DateTimeField() #datetime when the notification was created into the system -> this will be filled in the process of inserting the register from the Notifications table
    triggered_datetime = models.DateTimeField() #datetime when the conditions matched to trigger the notification. This is filled at the time of the INSERTION on this table.
    sent_datetime = models.DateTimeField() #datetime when the schedule lot processes this register. When this is filled, the register is DELETED from this table and INSERTED into NotificaitonHistory 

class NotificationHistory(models.Model):
    #TODO: Class to save the history of all triggered notifications in the plattform (to be able to analyze it by the system and to let the user see old alerts)
    notification_fk_id = ID FROM THE NOTIFICATION TABLE (the notification model holds the primary ID of every notification in the system) #-> this will be filled in the process of inserting the register from the Notifications table
    notification_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc
    user = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc 
    created_by = models.ForeignKey(Investor, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name, review null, on_delete, etc.
    created_datetime = models.DateTimeField() #datetime when the notification was created into the system 
    triggered_datetime = models.DateTimeField() #datetime when the conditions matched to trigger the notification.
    sent_datetime = models.DateTimeField() #datetime when the schedule lot processes this register.
    seen_datetime = models.DateTimeField() #datetime when the user have seen/clicked the notification on the frontend. THIS FIELD ONLY FILLED ON registers that come from FrontendQueue.!!! 
    #NOTE: Only FrontendQueue has the seen_datetime.

class PatternType(models.Model):
    #Class to define and add new types of chart patterns into the system. Only by admins.
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

class PatternConfig(models.Model):
    #Class to configure each type of pattern with the requeired parameters.
    #TODO: Revisar aquest model
    pattern_type = models.ForeignKey(PatternType, on_delete=models.DO_NOTHING, null=True, related_name="???") #TODO: Add related name
    json_config = models.JSONField() #With this JSON field we can add the requiered number and type of parameters for each patternType
'''