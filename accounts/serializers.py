from rest_framework import serializers
from .models import Account

# 조회
class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            # 'user',
            'account_name',
            'account_number',
            'bank_code',
            'is_primary',
            'created_at',
        ]

# 생성
class AccountsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'account_name',
            'account_number',
            'bank_code',
            'is_primary',
        ]

    def validate_account_number(self, data):
        if len(data) < 5:
            raise serializers.ValidationError('계좌번호는 5자리 이상이어야 합니다.')
        return data
