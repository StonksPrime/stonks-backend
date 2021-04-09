from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404
from django.db.models import Q
import simplejson as json

from ..models import Position, Crypto, Stock, ETF
from ..serializers import PositionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class PositionList(APIView):
    """
    List all positions
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, username, format=None):
        position = Position.objects.filter(user=request.user)
        serializer = PositionSerializer(position, many=True)
        return Response(serializer.data)

    def post(self, request, username, format=None):
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CryptoPositionList(APIView):
    """
    List all positions
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, username, format=None):
        cryptos = Crypto.objects.all()
        position = Position.objects.filter(user=request.user, asset__in=cryptos)
        not_empty_positions=position.exclude(quantity=0)
        
        positions = []
        for position in not_empty_positions:
            pos = {'assetName': position.asset.name, 'ticker': position.asset.ticker, 'broker': 'Kraken', 'type': 'crypto', 'market': 'Crypto', 
            'ownedShares': position.quantity,
                'value': 3049.2, 'totalValue': 6098.4, 'gains': 1647.57, 'gainsPercent': 27, 
                'comparison': { 'prevDate': 'M', 'prevValue': -15, 'nextDate': 'W', 'nextValue': 12 },
                'img': 'https://storage.googleapis.com/www-paredro-com/uploads/2019/04/bitcoin.jpg' 
                , 'BEP': position.break_even_price, 'todayGains': 15}
            positions.append(pos)


    
        data = json.dumps(positions)
        return HttpResponse(data, content_type='application/json')

class StockPositionList(APIView):
    """
    List all positions
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, username, format=None):
        stocks = Stock.objects.all()
        position = Position.objects.filter(user=request.user, asset__in=stocks)
        not_empty_positions=position.exclude(quantity=0)
        
        positions = []
        for position in not_empty_positions:
            diff = position.asset.last_price-position.break_even_price
            pos = {'assetName': position.asset.name, 'ticker': position.asset.ticker, 'broker': position.broker.name, 'type': 'stock', 
                'market': 'Nasdaq', 'ownedShares': position.quantity, 'value': position.asset.last_price, 
                'totalValue': round(position.asset.last_price*position.quantity,2), 
                'gains': round(diff * position.quantity,2), 
                'gainsPercent': round((diff/position.break_even_price)*100,2),
                'comparison': { 'prevDate': 'M', 'prevValue': -15, 'nextDate': 'W', 'nextValue': 12 },
                'img': position.asset.thumbnail_url
                , 'BEP': position.break_even_price, 'todayGains': 15}
            positions.append(pos)


    
        data = json.dumps(positions, use_decimal=True)
        return HttpResponse(data, content_type='application/json')

class ETFPositionList(APIView):
    """
    List all positions
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, username, format=None):
        stocks = ETF.objects.all()
        position = Position.objects.filter(user=request.user, asset__in=stocks)
        not_empty_positions=position.exclude(quantity=0)
        
        positions = []
        for position in not_empty_positions:
            diff = position.asset.last_price-position.break_even_price
            pos = {'assetName': position.asset.name, 'ticker': position.asset.ticker, 'broker': position.broker.name, 'type': 'ETF', 
                'market': 'Nasdaq', 'ownedShares': position.quantity, 'value': position.asset.last_price, 
                'totalValue': round(position.asset.last_price*position.quantity,2), 
                'gains': round(diff * position.quantity,2), 
                'gainsPercent': round((diff/position.break_even_price)*100,2),
                'comparison': { 'prevDate': 'M', 'prevValue': -15, 'nextDate': 'W', 'nextValue': 12 },
                'img': position.asset.thumbnail_url
                , 'BEP': position.break_even_price, 'todayGains': 15}
            positions.append(pos)

        data = json.dumps(positions, use_decimal=True)
        return HttpResponse(data, content_type='application/json')

class PositionDetail(APIView):
    """
    Retrieve, update or delete a position instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Position.objects.get(id=id)
        except Position.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        position = self.get_object(id)
        serializer = PositionSerializer(position)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        position = self.get_object(id)
        serializer = PositionSerializer(position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        position = self.get_object(id)
        position.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)