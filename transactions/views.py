from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing transactions (read-only)"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter transactions based on user permissions"""
        user = self.request.user
        
         # Swagger schema generation  error 
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()

        # AnonymousUser 
        if user.is_anonymous:
            return Transaction.objects.none()
        
        # Admin can see all transactions
        if user.is_staff:
            return Transaction.objects.all()
        
        # Regular users can only see transactions for their own invoices
        return Transaction.objects.filter(invoice__created_by=user)


