from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Position
from .brokers import kraken
# Create your views here.

@login_required
def positions(request):

	positions = Position.objects.filter(user=request.user)
	data = serializers.serialize('json', positions)

	return HttpResponse(data, content_type='application/json')

@login_required
def update_positions(request):

	api=kraken.KrakenAPI()
	api.loadInvestorAccount(request.user.username)
	api.updateCurrentPositions()

	return HttpResponse("{\"result\": \"ok\"}", content_type='application/json')