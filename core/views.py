from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Position, Broker, Account
from .brokers import kraken
from .serializers import UserSerializer, LogInSerializer

from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class LogInView(TokenObtainPairView): 
    serializer_class = LogInSerializer

@login_required
def positions(request):

	positions = Position.objects.filter(user=request.user)
	data = serializers.serialize('json', positions)

	return HttpResponse(data, content_type='application/json')

@login_required
def update_positions(request):
	accounts = Account.objects.filter(person=request.user)
	for account in accounts:
		broker = account.broker_exchange
		if broker.name == 'Kraken':
			api=kraken.KrakenAPI()
			api.loadInvestorAccount(request.user.username)
			api.updateCurrentPositions()

	return HttpResponse("{\"result\": \"ok\"}", content_type='application/json')