from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import Broker
from ..serializers import BrokerSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



class BrokerList(APIView):
    """
    List all brokers
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        broker = Broker.objects.all()
        serializer = BrokerSerializer(broker, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BrokerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BrokerDetail(APIView):
    """
    Retrieve, update or delete an broker instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Broker.objects.get(id=id)
        except Broker.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        broker = self.get_object(id)
        serializer = BrokerSerializer(broker)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        broker = self.get_object(id)
        serializer = BrokerSerializer(broker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        broker = self.get_object(id)
        broker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)