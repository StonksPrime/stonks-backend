from django.urls import path
from . import views

urlpatterns = [
    path('positions', views.positions, name='positions'),
    path('update_positions', views.update_positions, name='update_positions'),
]