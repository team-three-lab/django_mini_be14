from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Account

User = get_user_model()


class Analysis(models.Model):
    class AnalysisPeriod(models.TextChoices):
        DAILY = "DAILY", "일간"
        WEEKLY = "WEEKLY", "주간"
        MONTHLY = "MONTHLY", "월간"
        YEARLY = "YEARLY", "연간"

    user = models.ForeignKey(User, verbose_name="유저", on_delete=models.CASCADE)
    account = models.ForeignKey(Account, verbose_name="계좌", on_delete=models.CASCADE)
    is_income = models.BooleanField("수입 여부")
    period = models.CharField("분석 주기", max_length=20, choices=AnalysisPeriod.choices)
    start_date = models.DateTimeField("분석 시작 날짜")
    end_date = models.DateTimeField("분석 종료 날짜")
    description = models.TextField("분석 설명", blank=True)
    result_image = models.CharField("분석 결과 이미지", max_length=255, blank=True)
    is_active = models.BooleanField("활성 여부", default=True)
    last_run_at = models.DateTimeField("마지막 실행 시각", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.user}] {self.account} / {self.period}"
    
    class Meta:
        verbose_name = "분석"
        verbose_name_plural = "분석 목록"