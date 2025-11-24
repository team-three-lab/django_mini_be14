from django.contrib import admin
from .models import Transactions

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
     list_display = ['type', 'amount', 'created_at','balance','is_deposit']
     list_filter = ['type', 'created_at', 'is_deposit']
     search_fields = ['description']
     ordering = ['-created_at']