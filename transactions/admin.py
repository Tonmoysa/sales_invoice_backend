from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction"""
    list_display = ['id', 'invoice', 'transaction_type', 'amount', 'date']
    list_filter = ['transaction_type', 'date']
    search_fields = ['invoice__reference', 'invoice__customer_name']
    readonly_fields = ['date']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('invoice', 'transaction_type', 'amount', 'date')
        }),
    )


