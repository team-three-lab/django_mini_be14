from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from accounts.models import Account
from .serializers import TransactionListSerializer, TransactionCreateSerializer, TransactionDetailSerializer, TransactionUpdateSerializer




class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        transactions = Transaction.objects.filter(
            account__id=account_id,
            account__user=request.user).order_by("-created_at")
        

        search = request.query_params.get("search")
        if search:
            transactions = transactions.filter(description__icontains=search)
        
        type = request.query_params.get("type")
        if type:
            transactions = transactions.filter(transaction_type=type)

        serializer = TransactionListSerializer(instance=transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, account_id):
        account = get_object_or_404(Account, id=account_id, user=request.user)
        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(account=account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionRetrieveUpdateDestroyViewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, account_id):
        transaction = get_object_or_404(
            Transaction, 
            pk=pk,
            account__id=account_id,
            account__user=request.user
            )
        serializer = TransactionDetailSerializer(instance=transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, account_id):
        transaction = get_object_or_404(
            Transaction, 
            pk=pk,
            account__id=account_id,
            account__user=request.user
            )
        serializer = TransactionUpdateSerializer(instance=transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, account_id):
        transaction = get_object_or_404(
            Transaction, 
            pk=pk,
            account__id=account_id,
            account__user=request.user
            )
        transaction.delete()
        return Response({"msg":"Deleted"}, status=status.HTTP_200_OK)