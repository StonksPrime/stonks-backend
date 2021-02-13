from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import ETF
from ..serializers import ETFSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



class ETFList(APIView):
    """
    List all etfs
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        etf = ETF.objects.all()
        serializer = ETFSerializer(etf, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ETFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ETFDetail(APIView):
    """
    Retrieve, update or delete a etf instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return ETF.objects.get(id=id)
        except ETF.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        etf = self.get_object(id)
        serializer = ETFSerializer(etf)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        etf = self.get_object(id)
        serializer = ETFSerializer(etf, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        etf = self.get_object(id)
        etf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)