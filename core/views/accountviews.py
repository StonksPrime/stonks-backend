from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse,HttpResponse, Http404

from ..models import Account
from ..serializers import AccountSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class AccountList(APIView):
    """
    List all accounts
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        account = Account.objects.all()
        serializer = AccountSerializer(account, many=True)
        return Response(serializer.data)

class AccountDetail(APIView):
    """
    Retrieve, update or delete an Account instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Account.objects.get(id=id)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        account = self.get_object(id)
        serializer = AccountrSerializer(account)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        account = self.get_object(id)
        serializer = AccountrSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        account = self.get_object(id)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)