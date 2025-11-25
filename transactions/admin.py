from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionsAdmin(admin.ModelAdmin):
     list_display = ['amount', 'created_at','balance','is_deposit']
     list_filter = ['created_at', 'is_deposit']
     search_fields = ['description']
     ordering = ['-created_at']