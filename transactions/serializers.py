from rest_framework import serializers
from .models import Transaction

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','is_deposit','amount','description','transacted_at']

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount','description','balance','is_deposit','transaction_type','transacted_at']