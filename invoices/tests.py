from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
from rest_framework import status
from decimal import Decimal
from .models import Invoice, InvoiceItem


class InvoiceTestCase(TestCase):
    """Test cases for Invoice functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Authenticate user
        self.client.force_authenticate(user=self.user1)
    
    def test_create_invoice_success(self):
        """Test successful invoice creation"""
        data = {
            'reference': 'INV-001',
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'customer_phone': '1234567890',
            'items': [
                {
                    'name': 'Product 1',
                    'quantity': 2,
                    'price': '100.00'
                },
                {
                    'name': 'Product 2',
                    'quantity': 1,
                    'price': '50.00'
                }
            ]
        }
        
        response = self.client.post('/api/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        invoice = Invoice.objects.get(reference='INV-001')
        self.assertEqual(invoice.customer_name, 'John Doe')
        self.assertEqual(invoice.status, 'PENDING')
        self.assertEqual(invoice.total_amount, Decimal('250.00'))
        self.assertEqual(invoice.items.count(), 2)
        
        # Check that Sale transaction was created
        from transactions.models import Transaction
        transactions = Transaction.objects.filter(invoice=invoice, transaction_type='Sale')
        self.assertEqual(transactions.count(), 1)
    
    def test_create_invoice_no_items(self):
        """Test invoice creation with no items should fail"""
        data = {
            'reference': 'INV-002',
            'customer_name': 'Jane Doe',
            'items': []
        }
        
        response = self.client.post('/api/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_duplicate_reference(self):
        """Test that duplicate reference numbers are not allowed"""
        Invoice.objects.create(
            reference='INV-003',
            customer_name='Customer 1',
            total_amount=Decimal('100.00'),
            created_by=self.user1
        )
        
        data = {
            'reference': 'INV-003',
            'customer_name': 'Customer 2',
            'items': [
                {
                    'name': 'Product',
                    'quantity': 1,
                    'price': '100.00'
                }
            ]
        }
        
        response = self.client.post('/api/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_mark_invoice_as_paid(self):
        """Test marking an invoice as paid"""
        invoice = Invoice.objects.create(
            reference='INV-004',
            customer_name='Customer',
            total_amount=Decimal('100.00'),
            created_by=self.user1
        )
        
        InvoiceItem.objects.create(
            invoice=invoice,
            name='Product',
            quantity=1,
            price=Decimal('100.00')
        )
        
        # Create Sale transaction
        from transactions.models import Transaction
        Transaction.objects.create(
            invoice=invoice,
            transaction_type='Sale',
            amount=invoice.total_amount
        )
        
        response = self.client.patch(f'/api/invoices/{invoice.id}/pay/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, 'PAID')
        
        # Check that Payment transaction was created
        payment_transactions = Transaction.objects.filter(
            invoice=invoice,
            transaction_type='Payment'
        )
        self.assertEqual(payment_transactions.count(), 1)
    
    def test_cannot_pay_non_pending_invoice(self):
        """Test that only pending invoices can be marked as paid"""
        invoice = Invoice.objects.create(
            reference='INV-005',
            customer_name='Customer',
            total_amount=Decimal('100.00'),
            status='PAID',
            created_by=self.user1
        )
        
        response = self.client.patch(f'/api/invoices/{invoice.id}/pay/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_sees_only_own_invoices(self):
        """Test that users can only see their own invoices"""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        invoice1 = Invoice.objects.create(
            reference='INV-006',
            customer_name='Customer 1',
            total_amount=Decimal('100.00'),
            created_by=self.user1
        )
        
        invoice2 = Invoice.objects.create(
            reference='INV-007',
            customer_name='Customer 2',
            total_amount=Decimal('200.00'),
            created_by=user2
        )
        
        response = self.client.get('/api/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['reference'], 'INV-006')
    
    def test_admin_sees_all_invoices(self):
        """Test that admin users can see all invoices"""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        Invoice.objects.create(
            reference='INV-008',
            customer_name='Customer 1',
            total_amount=Decimal('100.00'),
            created_by=self.user1
        )
        
        Invoice.objects.create(
            reference='INV-009',
            customer_name='Customer 2',
            total_amount=Decimal('200.00'),
            created_by=user2
        )
        
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get('/api/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users cannot access invoice APIs"""
        self.client.force_authenticate(user=None)
        
        response = self.client.get('/api/invoices/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.post('/api/invoices/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


