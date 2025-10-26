from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Invoice(models.Model):
    """Invoice model for managing sales invoices"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    ]
    
    reference = models.CharField(max_length=100, unique=True, db_index=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=50, blank=True, null=True)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'invoices'
    
    def __str__(self):
        return f"Invoice {self.reference} - {self.customer_name}"
    
    def clean(self):
        if self.total_amount < 0:
            raise ValidationError("Total amount cannot be negative")


class InvoiceItem(models.Model):
    """Items within an invoice"""
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        db_table = 'invoice_items'
    
    def __str__(self):
        return f"{self.name} - {self.quantity}x"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.quantity * self.price
    
    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1")


