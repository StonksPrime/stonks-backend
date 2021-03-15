from django.urls import path
from .views.assetviews import AssetDetail, AssetList
from .views.brokerviews import BrokerDetail, BrokerList
from .views.accountviews import AccountDetail, AccountList
from .views.stockviews import StockDetail, StockList, StockListApple
from .views.fiatviews import FiatDetail, FiatList
from .views.positionviews import PositionDetail, PositionList
from .views.fundviews import FundDetail, FundList
from .views.etfviews import ETFDetail, ETFList
from .views.cryptoviews import CryptoDetail, CryptoList
from .views.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('investors/', InvestorList.as_view()),
    path('investors/<username>/', InvestorDetail.as_view()),

    path('assets/', AssetList.as_view()),
    path('assets/<ticker>/', AssetDetail.as_view()),

    path('brokers/', BrokerList.as_view()),
    path('brokers/<id>/', BrokerDetail.as_view()),

    path('accounts/', AccountList.as_view()),
    path('accounts/<id>/', AccountDetail.as_view()),

    path('stocks/', StockList.as_view()),
    path('stocksapple/', StockListApple.as_view()),
    path('stocks/<id>/', StockDetail.as_view()),

    path('fiats/', FiatList.as_view()),
    path('fiats/<id>/', FiatDetail.as_view()),

    path('funds/', FundList.as_view()),
    path('funds/<id>/', FundDetail.as_view()),

    path('etfs/', ETFList.as_view()),
    path('etfs/<id>/', ETFDetail.as_view()),

    path('cryptos/', CryptoList.as_view()),
    path('cryptos/<id>/', CryptoDetail.as_view()),

    path('positions_class/', PositionList.as_view()),
    path('positions_class/<id>/', PositionDetail.as_view()),

    path('token-auth/', LogInView.as_view(), name='log_in'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

    path('positions/', positions, name='positions'),
    path('update_positions/', update_positions, name='update_positions'),
]