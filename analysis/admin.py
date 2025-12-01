from django.contrib import admin
from .models import Analysis

class AnalysisAdmin(admin.ModelAdmin):
    list_display = ["user","account" , "is_income", "start_date", "end_date"]
    list_filter = ["account", "is_income"]
    search_fields = ["user"]