from rest_framework import serializers
from .models import Transaction

class TransactionListSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["id","transaction_type", "is_deposit", "amount", "description", "transacted_at"]

    def get_description(self, obj):
        value = obj.description or ""
        if len(value) > 10:
            value = value[:10] + "..."
            return value
        return value


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Transaction
        fields = [
            "amount",
            "balance",
            "description",
            "is_deposit",
            "transaction_type",
            "transacted_at"
            ]
        


class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "amount",
            "balance",
            "description",
            "is_deposit",
            "transaction_type",
            "transacted_at"
            ]


class TransactionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

