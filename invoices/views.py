from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Invoice
from .serializers import InvoiceReadSerializer, InvoiceWriteSerializer, InvoiceStatusUpdateSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing invoices"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceReadSerializer
    
    def get_queryset(self):
        """Filter invoices based on user permissions"""
        user = self.request.user
        
        # Admin can see all invoices
        if user.is_staff:
            return Invoice.objects.all()
        
        # Regular users can only see their own invoices
        return Invoice.objects.filter(created_by=user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return InvoiceWriteSerializer
        return InvoiceReadSerializer
    
    def perform_create(self, serializer):
        """Create invoice with proper validation"""
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        """Override update to handle status changes only"""
        instance = self.get_object()
        
        # Check if only status is being updated
        if 'status' in request.data and len(request.data) == 1:
            serializer = InvoiceStatusUpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # For other updates, only status can be changed
        if any(key != 'status' for key in request.data.keys()):
            return Response(
                {'error': 'Only status field can be updated. Customer info and items cannot be modified after creation.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['patch'])
    def pay(self, request, pk=None):
        """Custom action to mark invoice as paid"""
        invoice = self.get_object()
        
        if invoice.status != 'PENDING':
            return Response(
                {'error': 'Only pending invoices can be marked as paid.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update status
        invoice.status = 'PAID'
        invoice.save()
        
        # Create Payment transaction
        from transactions.models import Transaction
        Transaction.objects.create(
            invoice=invoice,
            transaction_type='Payment',
            amount=invoice.total_amount
        )
        
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)


