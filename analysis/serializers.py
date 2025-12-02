from rest_framework import serializers
from .models import Analysis
from accounts.models import Account

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = [
            "id",
            "user",
            "account",
            "is_income",
            "period",
            "start_date",
            "end_date",
            "description",
            "result_image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate_account(self, accounts):
        """
        선택된 계좌가 요청한 유저의 계좌가 맞는지 확인
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if accounts.user != request.user:
                raise serializers.ValidationError("본인 소유 계좌만 분석할 수 있습니다.")
        return accounts
    
    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        if start and end and start > end:
            raise serializers.ValidationError("분석 시작 날짜와 종료 날짜가 올바르지 않습니다.")
        return attrs
    
    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)