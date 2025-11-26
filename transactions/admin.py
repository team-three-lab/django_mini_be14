from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
     list_display = ["account__account_name", "is_deposit", "transacted_at"]
     list_filter = ["account_id__account_name", "is_deposit", "transacted_at"]
     search_fields = ["description"]
     ordering = ['-created_at']