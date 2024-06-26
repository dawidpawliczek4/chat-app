from django.shortcuts import render
from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer
from rest_framework.response import Response

# Create your views here.
class AccountViewSet(viewsets.ViewSet):
    # queryset = Account.objects.all()
    def list(self, request):        
        user_id = request.query_params.get('user_id')
        queryset = Account.objects.get(user_id=user_id)
        serializer = AccountSerializer(queryset)
        return Response(serializer.data)