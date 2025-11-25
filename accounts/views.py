from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountsSimpleSerializer, AccountsCreateSerializer, AccountRetrieveSerializer,  AccountDestroySerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAccountOwner

# Create your views here.
class AccountListCreateView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        accounts = Account.objects.filter(user=request.user) 
        serializer = AccountsSimpleSerializer(instance=accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = AccountsCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_object(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        self.check_object_permissions(request, account)
        return account

    def get(self, request, pk):
        account = self.get_object(request, pk)
        serializer = AccountRetrieveSerializer(instance=account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, pk):
        account = self.get_object(request, pk)
        account_id = account.id
        account_name = account.account_name
        serialzier = AccountDestroySerializer(instance=account)
        account.delete()
        return Response(
            {
                "message": "계좌가 삭제되었습니다.",
                "account_id": account_id,
                "account_name": account_name,
            }, status=status.HTTP_200_OK)