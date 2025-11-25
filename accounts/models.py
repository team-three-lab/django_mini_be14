from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Account(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255, unique=True)
    bank_code = models.CharField(max_length=255, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.user}의 {self.account_name}"

