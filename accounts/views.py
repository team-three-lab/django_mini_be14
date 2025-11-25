from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Account
from .serializers import AccountsSerializer, AccountsCreateSerializer
from rest_framework.permissions import IsAuthenticated

class AccountListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountsSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AccountsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountsSerializer(account) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        account = get_object_or_404(Account, pk=pk)

        # account = get_object_or_404(Account, pk=pk, user=request.user)

        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)