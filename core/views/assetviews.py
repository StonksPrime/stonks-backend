from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import Asset
from ..serializers import AssetSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class AssetList(APIView):
    """
    List all assets
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        asset = Asset.objects.all()
        serializer = AssetSerializer(asset, many=True)
        return Response(serializer.data)

class AssetDetail(APIView):
    """
    Retrieve, update or delete an asset instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, ticker):
        try:
            return Asset.objects.get(ticker=ticker)
        except Asset.DoesNotExist:
            raise Http404

    def get(self, request, ticker, format=None):
        asset = self.get_object(ticker)
        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    def put(self, request, ticker, format=None):
        asset = self.get_object(ticker)
        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticker, format=None):
        asset = self.get_object(ticker)
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)