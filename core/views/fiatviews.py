from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import Fiat
from ..serializers import FiatSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class FiatList(APIView):
    """
    List all fiats
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        fiat = Fiat.objects.all()
        serializer = FiatSerializer(fiat, many=True)
        return Response(serializer.data)

class FiatDetail(APIView):
    """
    Retrieve, update or delete a fiat instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Fiat.objects.get(id=id)
        except Fiat.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        fiat = self.get_object(id)
        serializer = FiatSerializer(fiat)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        fiat = self.get_object(id)
        serializer = FiatSerializer(fiat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        fiat = self.get_object(id)
        fiat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)