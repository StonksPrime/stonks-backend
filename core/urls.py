from django.urls import path
from . import views
from .views import SignUpView, LogInView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('positions/', views.positions, name='positions'),
    path('update_positions/', views.update_positions, name='update_positions'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('log_in/', LogInView.as_view(), name='log_in'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]