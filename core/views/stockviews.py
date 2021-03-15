from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import Stock
from ..serializers import StockSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import finnhub
from ..secret_api_tokens import *

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

class StockListApple(APIView):
    def get(self, request, format=None):
        return Response(finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249), status=status.HTTP_200_OK)


class StockList(APIView):
    """
    List all stocks
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        stock = Stock.objects.all()
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockDetail(APIView):
    """
    Retrieve, update or delete an Stock instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Stock.objects.get(id=id)
        except Stock.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        stock = self.get_object(id)
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        stock = self.get_object(id)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        stock = self.get_object(id)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)