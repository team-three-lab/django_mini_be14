from django.contrib import admin
from .models import Account

# Register your models here.
@admin.register(Account)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ["user", "account_name"]
    list_filter = ["user", "account_name"]
    search_fields = ["user__username", "account_name"]
    search_help_text = "회원 아이디, 계좌 용도로 검색이 가능합니다."