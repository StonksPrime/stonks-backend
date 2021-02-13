from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import Position
from ..serializers import PositionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PositionList(APIView):
    """
    List all positions
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        position = Position.objects.filter(user=request.user)
        serializer = PositionSerializer(position, many=True)
        return Response(serializer.data)

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