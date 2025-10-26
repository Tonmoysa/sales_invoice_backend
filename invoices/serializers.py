from rest_framework import serializers
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models import Invoice, InvoiceItem

User = get_user_model()


class InvoiceItemSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceItem"""
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = InvoiceItem
        fields = ['id', 'name', 'quantity', 'price', 'subtotal']


class InvoiceReadSerializer(serializers.ModelSerializer):
    """Serializer for reading Invoice (includes full details)"""
    items = InvoiceItemSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'reference', 'customer_name', 'customer_email', 'customer_phone',
            'total_amount', 'status', 'created_by', 'created_at', 'updated_at',
            'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_amount']


class InvoiceWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Invoice"""
    items = InvoiceItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'reference', 'customer_name', 'customer_email', 'customer_phone',
            'total_amount', 'status', 'created_by', 'created_at', 'updated_at',
            'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_amount', 'created_by']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Validate at least one item exists
        if not items_data:
            raise serializers.ValidationError({
                'items': 'Invoice must have at least one item.'
            })
        
        # Calculate total first
        total = Decimal('0.00')
        for item_data in items_data:
            total += Decimal(str(item_data['quantity'])) * Decimal(str(item_data['price']))
        
        # Get the user from the request context
        user = self.context['request'].user
        
        # Create invoice with calculated total
        invoice = Invoice.objects.create(
            created_by=user,
            total_amount=total,
            **validated_data
        )
        
        # Create invoice items
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        
        # Create Sale transaction
        from transactions.models import Transaction
        Transaction.objects.create(
            invoice=invoice,
            transaction_type='Sale',
            amount=invoice.total_amount
        )
        
        return invoice
    
    def update(self, instance, validated_data):
        # Only allow updating status for pending invoices
        if 'status' in validated_data:
            if validated_data['status'] == 'PAID' and instance.status != 'PENDING':
                raise serializers.ValidationError({
                    'status': 'Only pending invoices can be marked as paid.'
                })
        
        # Update only status
        if 'status' in validated_data:
            instance.status = validated_data['status']
            instance.save()
            
            # If marking as paid, create Payment transaction
            if validated_data['status'] == 'PAID':
                from transactions.models import Transaction
                Transaction.objects.create(
                    invoice=instance,
                    transaction_type='Payment',
                    amount=instance.total_amount
                )
        
        return instance


class InvoiceStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer specifically for updating invoice status"""
    
    class Meta:
        model = Invoice
        fields = ['status']
    
    def validate_status(self, value):
        if self.instance and self.instance.status != 'PENDING' and value == 'PAID':
            raise serializers.ValidationError('Only pending invoices can be marked as paid.')
        return value

