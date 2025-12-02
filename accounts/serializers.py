from rest_framework import serializers
from .models import Account


class AccountsSimpleSerializer(serializers.ModelSerializer):
    """
    계좌번호 리스트 페이지 시리얼라이저
    """
    masked_account_number = serializers.SerializerMethodField()
    bank_name = serializers.CharField(
    source="get_bank_code_display", read_only=True
    )

    
    class Meta:
        model = Account
        fields = [
            'id',
            'account_name',
            'bank_code',
            'bank_name',
            'is_primary',
            'masked_account_number'
        ]

    def get_masked_account_number(self, obj: Account) -> str:
        """
        계좌번호 뒷 4자리만 남기고 앞은 * 처리
        """
        num = obj.account_number
        if len(num) <= 4:
            return num
        return "*" * (len(num) - 4) + num[-4:]


class AccountsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        """
        사용자가 지정된 값을 넣을 수 있도록, 그리고 계좌번호에 올바른 양식을 넣을 수 있도록
        검증을 해주는 시리얼라이저
        """
        model = Account
        fields = [
            'account_name',
            'account_number',
            'bank_code',
            # 'account_type',
            # 'balance',
            'is_primary',
        ]

    def validate_account_number(self, value: str) -> str:
        
        cleaned = value.replace(" ", "").replace("-", "")
        if not cleaned.isdigit():
            raise serializers.ValidationError("계좌번호는 숫자와 '-'만 사용할 수 있습니다.")
        
        if not (10 <= len(cleaned) <= 14):
            raise serializers.ValidationError("계좌번호 자리수가 올바르지 않습니다.")
        
        return cleaned


class AccountRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"



class AccountDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_number', 'account_name', 'user', 'id']