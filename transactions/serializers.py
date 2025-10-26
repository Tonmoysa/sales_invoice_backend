from rest_framework import serializers
from .models import Transaction
from invoices.serializers import InvoiceReadSerializer


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    invoice = InvoiceReadSerializer(read_only=True)
    invoice_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Transaction
        fields = ['id', 'invoice', 'invoice_id', 'transaction_type', 'amount', 'date']
        read_only_fields = ['id', 'date']

