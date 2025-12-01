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
    """
    생성용: balance 는 사용자가 안 보내고 서버에서 계산
    """
    class Meta:
        model = Transaction
        fields = [
            "amount",
            "description",
            "is_deposit",
            "transaction_type",
            "transacted_at",
        ]

    def create(self, validated_data):
        from .models import Transaction  # 순환 import 방지용 (안전빵)

        account = self.context["account"]

        last_tx = (
            Transaction.objects.filter(account=account)
            .order_by("-transacted_at", "-id")
            .first()
        )
        prev_balance = last_tx.balance if last_tx else 0

        amount = validated_data["amount"]
        is_deposit = validated_data["is_deposit"]

        if is_deposit:
            new_balance = prev_balance + amount
        else:
            if prev_balance < amount:
                raise serializers.ValidationError("잔액이 부족합니다.")
            new_balance = prev_balance - amount

        validated_data["account"] = account
        validated_data["balance"] = new_balance

        return super().create(validated_data)
        


def recalc_account_balances(account):
    """
    특정 계좌의 모든 거래에 대해 balance를 재계산.
    (수정/삭제 이후에 호출)
    """
    qs = Transaction.objects.filter(account=account).order_by(
        "transacted_at", "id"
    )
    balance = 0
    for tx in qs:
        if tx.is_deposit:
            balance += tx.amount
        else:
            balance -= tx.amount
        tx.balance = balance
        tx.save(update_fields=["balance"])


class TransactionUpdateSerializer(serializers.ModelSerializer):
    """
    수정용: amount / is_deposit / type 바꾸면 잔액들 전체 재계산
    """
    class Meta:
        model = Transaction
        fields = [
            "amount",
            "description",
            "is_deposit",
            "transaction_type",
            "transacted_at",
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        from .serializers import recalc_account_balances as _recalc

        _recalc(instance.account)
        instance.refresh_from_db()
        return instance


class TransactionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"