from django.db import models
from django.core.validators import MinValueValidator
from invoices.models import Invoice


class Transaction(models.Model):
    """Transaction model to track sales and payments"""
    
    TRANSACTION_TYPES = [
        ('Sale', 'Sale'),
        ('Payment', 'Payment'),
    ]
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        db_table = 'transactions'
    
    def __str__(self):
        return f"{self.transaction_type} - {self.invoice.reference} - ${self.amount}"
    
    def clean(self):
        if self.amount < 0:
            from django.core.exceptions import ValidationError
            raise ValidationError("Amount cannot be negative")


