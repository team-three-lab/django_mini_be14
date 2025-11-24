from rest_framework import serializers
from .models import Transactions

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'

from rest_framework import serializers
from .models import Transactions


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"
        # DB에서 자동으로 정해지는 값들은 수정 못하게 read_only로 두는 게 좋음
        read_only_fields = ("id", "created_at", "updated_at")
        # 만약 created_at, updated_at 필드가 없다면 위 두 개는 빼도 됨
