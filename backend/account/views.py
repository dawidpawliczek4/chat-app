from django.shortcuts import render
from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer

# Create your views here.

class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created"}, status=201)
        return Response(serializer.errors, status=400)

class AccountViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):        
        user_id = request.query_params.get('user_id')
        queryset = Account.objects.get(id=user_id)
        serializer = AccountSerializer(queryset)
        return Response(serializer.data)