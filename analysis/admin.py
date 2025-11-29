from django.contrib import admin
from .models import Analysis

class AnalysisAdmin(admin.ModelAdmin):
    list_display = ["user","trnsactioin" , "is_income", "start_date", "end_date"]
    list_filter = ["transaction", "is_income"]
    search_fields = ["user"]