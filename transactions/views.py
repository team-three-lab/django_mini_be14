from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Transactions
from .serializers import TransactionsSerializer

class TransactionListCreateView(APIView):
    def get (self, request):
        transaction = Transactions.objects.all()
        serilalzier = TransactionsSerializer(transaction, many=True)
        return Response(serilalzier.data, status=status.HTTP_200_OK)
    



class TransactionListCreateView(APIView):
    # 전체 목록 + 생성

    def get(self, request):
        """
        거래 내역 리스트 조회
        ?type=DEPOSIT 또는 ?type=WITHDRAW 로 필터링 가능
        """
        queryset = Transactions.objects.all()

        # 쿼리 파라미터로 타입 필터링 (선택사항)
        tx_type = request.query_params.get("type")
        if tx_type:
            queryset = queryset.filter(type=tx_type)

        serializer = TransactionsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        거래 내역 생성
        """
        serializer = TransactionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 유효하면 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    # 단일 거래 조회 / 수정 / 삭제

    def get_object(self, pk):
        # pk(기본키)로 객체 한 개 가져오기, 없으면 404
        return get_object_or_404(Transactions, pk=pk)

    def get(self, request, pk):
        """
        단일 거래 조회
        """
        transaction = self.get_object(pk)
        serializer = TransactionsSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        단일 거래 전체 수정
        """
        transaction = self.get_object(pk)
        serializer = TransactionsSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        단일 거래 삭제
        """
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
