from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import Crypto
from ..serializers import CryptoSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CryptoList(APIView):
    """
    List all cryptos
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        crypto = Crypto.objects.all()
        serializer = CryptoSerializer(crypto, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CryptoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CryptoDetail(APIView):
    """
    Retrieve, update or delete a crypto instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Crypto.objects.get(id=id)
        except Crypto.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        crypto = self.get_object(id)
        serializer = CryptoSerializer(crypto)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        crypto = self.get_object(id)
        serializer = CryptoSerializer(crypto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        crypto = self.get_object(id)
        crypto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)