from django.db import models 

class Accounts(models.Model):
    TYPE = (
        ("DEPOSIT", "입금"),
        ("WITHDRAW" "출금"),
    )

    # account_id = models.IntegerField() #나중에 fk로 연결 할 계획
    type = models.CharField(max_length=20, choices=TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    result_amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"타입: {self.type}, {self.type}금액: {self.amount}"
    
    class Meta:
        db_table = "accounts"
        verbose_name = "계좌 조회"
        verbose_name_plural = "조회 목록"