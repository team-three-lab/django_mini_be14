from django.db import models 

class Transactions(models.Model):
    TYPE = (
        ("DEPOSIT", "입금"),
        ("WITHDRAW", "출금"),
        ("TRANSFER", "이체"),
        ("PAYMENT", "결제"),
        ("REFUND", "환불"),
        ("CARD","카드 결제"),
        ("OTHER", "기타"),
        ("ATM", "ATM 거래"),
    )

    # account_id = models.IntegerField() #나중에 fk로 연결 할 계획
    type = models.CharField(max_length=20, choices=TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    result_amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.IntegerField()
    description = models.CharField(
        max_length=255,
        blank=True,
      
    )
    is_deposit = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.type
    
    class Meta:
        db_table = "transactions"
        verbose_name = "거래 내역"
        verbose_name_plural = "거래 내역 목록"
        ordering = ["-created_at"] 
