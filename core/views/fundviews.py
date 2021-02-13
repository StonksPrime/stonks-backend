from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import Fund
from ..serializers import FundSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class FundList(APIView):
    """
    List all funds
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        fund = Fund.objects.all()
        serializer = FundSerializer(fund, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FundDetail(APIView):
    """
    Retrieve, update or delete a fund instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Fund.objects.get(id=id)
        except Fund.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        fund = self.get_object(id)
        serializer = FundSerializer(fund)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        fund = self.get_object(id)
        serializer = FundSerializer(fund, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        fund = self.get_object(id)
        fund.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)