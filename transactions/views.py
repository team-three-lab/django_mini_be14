from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Transaction
from .serializers import TransactionsSerializer, TransactionCreateSerializer

class TransactionListCreateView(APIView):
    def get (self, request):
        transaction = Transaction.objects.all()
        serilalzier = TransactionsSerializer(transaction, many=True)
        return Response(serilalzier.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)