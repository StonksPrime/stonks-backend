from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from ..models import Position, Broker, Account, Investor
from ..brokers import kraken
from ..serializers import InvestorSerializer, UserSerializer, LogInSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


#TODO: merge UserSerializer with InvestorSerializer?
class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class LogInView(TokenObtainPairView): 
    serializer_class = LogInSerializer

class InvestorList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        investor = Investor.objects.all()
        serializer = InvestorSerializer(investor, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InvestorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvestorDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = (IsAuthenticated,)
    def get_object(self, username):
        try:
            return Investor.objects.get(username=username)
        except Investor.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        investor = self.get_object(username)
        serializer = InvestorSerializer(investor)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        investor = self.get_object(username)
        serializer = InvestorSerializer(investor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        investor = self.get_object(username)
        investor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#TODO: refactor to class based view
@login_required
def positions(request):

	positions = Position.objects.filter(user=request.user)
	data = serializers.serialize('json', positions)

	return HttpResponse(data, content_type='application/json')


#TODO: refactor to class based view
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