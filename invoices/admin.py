from django.contrib import admin
from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    """Inline admin for InvoiceItem"""
    model = InvoiceItem
    extra = 1
    fields = ['name', 'quantity', 'price']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Admin interface for Invoice"""
    list_display = ['reference', 'customer_name', 'total_amount', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reference', 'customer_name', 'customer_email']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        ('Invoice Details', {
            'fields': ('reference', 'status', 'total_amount', 'created_by')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    """Admin interface for InvoiceItem"""
    list_display = ['invoice', 'name', 'quantity', 'price', 'subtotal']
    search_fields = ['name', 'invoice__reference']


