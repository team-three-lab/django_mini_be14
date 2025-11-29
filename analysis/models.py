from django.db import models
from django.contrib.auth import get_user_model
from transactions.models import Transaction

User = get_user_model()

# Create your models here.

class Analysis(models.Model):
    ANALYSIS_TYPES = [
    ("DAILY", "일간"),
    ("WEEKLY", "주간"),
    ("MONTHLY", "월간"),
    ("YEARLY", "연간"),
    ]
    user = models.ForeignKey(User,verbose_name="유저", on_delete=models.CASCADE)
    transactions = models.ForeignKey(Transaction,verbose_name="계좌" , on_delete=models.CASCADE)
    is_income = models.BooleanField("분석 대상")
    periiod = models.CharField("분석 기간", max_length=255, choices=ANALYSIS_TYPES)
    end_date = models.DateTimeField("분석 시작 날자")
    start_date = models.DateTimeField("분석 종료 날짜")
    description = models.TextField("분석 설명")
    result_image = models.CharField("분석 결과",max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user
    
    class Meta:
        verbose_name = "분석"
        verbose_name_plural = "분석 목록"