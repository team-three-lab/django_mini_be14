from django.db import models


# Create your models here.
class Transaction(models.Model):

   #account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    amount = models.IntegerField("거래 금액")
    balance = models.IntegerField("거래 후 잔액")
    description = models.CharField("거래 내역",max_length=255)
    is_deposit = models.BooleanField("입출금 타입")
    transaction_type = models.CharField("거래 타입",max_length=255)
    transacted_at = models.DateTimeField("거래 일시")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


   # def __str__(self):
      #  return self.account.account_name
    
    class Meta:
        db_table = "transaction"
        verbose_name = "계좌 조회"
        verbose_name_plural = "조회 목록"