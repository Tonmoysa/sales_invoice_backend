# Sales Invoice Management System

A comprehensive Django REST Framework backend system for managing sales invoices and recording related transactions. This system provides secure user authentication, complete invoice lifecycle management, automatic transaction tracking, and detailed API documentation.

## 🎯 Project Overview

This backend system fulfills all the specified requirements for a sales invoice management system:

- ✅ **Invoice Management**: Create, update, view, and manage invoices with customer details
- ✅ **Transaction Tracking**: Automatic recording of Sale and Payment transactions
- ✅ **JWT Authentication**: Secure token-based authentication for all API endpoints
- ✅ **Business Logic**: Auto-calculated totals, validation rules, and status management
- ✅ **API Documentation**: Complete Swagger/OpenAPI documentation
- ✅ **Data Validation**: Comprehensive input validation and error handling

## 🚀 Core Features

### Invoice Management
- **Create Invoices**: Add new invoices with customer details and multiple line items
- **View Invoices**: List and retrieve detailed invoice information
- **Update Invoices**: Modify invoice status and basic information
- **Payment Processing**: Mark invoices as paid with automatic transaction recording
- **Auto-calculation**: Total amounts automatically calculated from line items

### Transaction Tracking
- **Sale Transactions**: Automatically created when invoices are generated
- **Payment Transactions**: Automatically created when invoices are marked as paid
- **Transaction History**: Complete audit trail of all financial activities
- **Read-only Access**: Transaction records are immutable for data integrity

### User Authentication & Security
- **JWT Authentication**: Secure token-based authentication system
- **User Registration**: Self-service user account creation
- **Role-based Access**: Different permissions for regular users and admins
- **Password Validation**: Django's built-in password security validators

## 🏗️ System Architecture

### Database Models

#### User Model (`users.User`)
- Extended Django's AbstractUser with email as unique identifier
- Custom user model for authentication and authorization
- Supports first_name, last_name, email, and username fields

#### Invoice Model (`invoices.Invoice`)
- **Core Fields**: reference (unique), customer_name, customer_email, customer_phone
- **Financial Fields**: total_amount (auto-calculated), status (PENDING/PAID)
- **Audit Fields**: created_by, created_at, updated_at
- **Validation**: Non-negative amounts, unique references, required fields

#### InvoiceItem Model (`invoices.InvoiceItem`)
- **Fields**: invoice (FK), name, quantity, price
- **Calculated Properties**: subtotal (quantity × price)
- **Validation**: Positive quantities and prices, minimum quantity of 1

#### Transaction Model (`transactions.Transaction`)
- **Fields**: invoice (FK), transaction_type (Sale/Payment), amount, date
- **Purpose**: Track all financial activities related to invoices
- **Validation**: Non-negative amounts, required transaction types

### API Endpoints

#### Authentication Endpoints
```
POST /api/token/                    # Obtain JWT access token
POST /api/token/refresh/            # Refresh access token
POST /api/token/verify/             # Verify token validity
```

#### User Management
```
POST /api/users/register/           # Register new user
GET  /api/users/profile/            # Get current user profile
```

#### Invoice Management
```
GET    /api/invoices/               # List all invoices (user-filtered)
POST   /api/invoices/               # Create new invoice
GET    /api/invoices/{id}/          # Get invoice details
PATCH  /api/invoices/{id}/          # Update invoice (status only)
PATCH  /api/invoices/{id}/pay/      # Mark invoice as paid
DELETE /api/invoices/{id}/          # Delete invoice
```

#### Transaction Management
```
GET /api/transactions/              # List all transactions (read-only)
GET /api/transactions/{id}/         # Get transaction details
```

#### API Documentation
```
GET /swagger/                       # Interactive Swagger UI
GET /redoc/                         # Alternative ReDoc documentation
GET /swagger.json/                  # OpenAPI schema (JSON)
```

## 🛠️ Technology Stack

- **Backend Framework**: Django 5.2.7
- **API Framework**: Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt 5.5.1)
- **API Documentation**: drf-yasg 1.21.11
- **CORS Support**: django-cors-headers 4.9.0
- **Database**: SQLite (development), PostgreSQL ready
- **Static Files**: WhiteNoise 6.11.0
- **Configuration**: python-decouple 3.8

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git (for version control)

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Tonmoysa/sales_invoice_backend.git
cd sales_invoice_backend
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📖 API Usage Examples

### Authentication Flow

#### 1. Register a New User
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

#### 2. Login and Get JWT Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Invoice Operations

#### 1. Create a New Invoice
```bash
curl -X POST http://127.0.0.1:8000/api/invoices/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reference": "INV-2024-001",
    "customer_name": "Acme Corporation",
    "customer_email": "contact@acme.com",
    "customer_phone": "+1234567890",
    "items": [
      {
        "name": "Web Development Services",
        "quantity": 10,
        "price": "1500.00"
      },
      {
        "name": "UI/UX Design",
        "quantity": 5,
        "price": "800.00"
      }
    ]
  }'
```

**Response:**
```json
{
  "id": 1,
  "reference": "INV-2024-001",
  "customer_name": "Acme Corporation",
  "customer_email": "contact@acme.com",
  "customer_phone": "+1234567890",
  "total_amount": "19000.00",
  "status": "PENDING",
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "items": [
    {
      "id": 1,
      "name": "Web Development Services",
      "quantity": 10,
      "price": "1500.00",
      "subtotal": "15000.00"
    },
    {
      "id": 2,
      "name": "UI/UX Design",
      "quantity": 5,
      "price": "800.00",
      "subtotal": "4000.00"
    }
  ]
}
```

#### 2. Mark Invoice as Paid
```bash
curl -X PATCH http://127.0.0.1:8000/api/invoices/1/pay/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 3. List All Invoices
```bash
curl -X GET http://127.0.0.1:8000/api/invoices/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Transaction Operations

#### View All Transactions
```bash
curl -X GET http://127.0.0.1:8000/api/transactions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔒 Business Logic & Validation

### Invoice Validation Rules
- ✅ **Unique References**: Each invoice must have a unique reference number
- ✅ **Minimum Items**: Invoice must have at least one item
- ✅ **Non-negative Amounts**: All amounts must be non-negative
- ✅ **Auto-calculation**: Total amount automatically calculated from items
- ✅ **Status Validation**: Payment only allowed for PENDING invoices

### Transaction Rules
- ✅ **Automatic Creation**: Sale transaction created when invoice is created
- ✅ **Payment Tracking**: Payment transaction created when invoice is marked as paid
- ✅ **Immutable Records**: Transactions cannot be modified after creation
- ✅ **Amount Consistency**: Transaction amounts match invoice totals

### User Access Control
- ✅ **Authentication Required**: All API endpoints require valid JWT token
- ✅ **User Isolation**: Regular users can only access their own invoices
- ✅ **Admin Access**: Admin users can access all invoices and transactions
- ✅ **Token Security**: JWT tokens expire after 2 hours (configurable)

## 🧪 Testing

### Run Test Suite
```bash
python manage.py test
```

### Test Coverage
The system includes comprehensive tests for:
- User registration and authentication
- Invoice creation and validation
- Payment processing and transaction creation
- Permission-based access control
- Data validation and error handling
- API endpoint functionality

### Manual Testing
Use the provided Postman collection (`Sales_Invoice_API.postman_collection.json`) for comprehensive API testing.

## 📊 Database Schema

### Tables Overview
- **users**: User accounts and authentication
- **invoices**: Invoice records with customer information
- **invoice_items**: Line items for each invoice
- **transactions**: Financial transaction history

### Key Relationships
- User → Invoices (One-to-Many)
- Invoice → InvoiceItems (One-to-Many)
- Invoice → Transactions (One-to-Many)

## 🔧 Configuration

### JWT Settings
- **Access Token Lifetime**: 2 hours
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled
- **Blacklist After Rotation**: Enabled
- **Algorithm**: HS256

### CORS Configuration
- **Development**: All origins allowed (for testing)
- **Production**: Configure specific allowed origins

### Pagination
- **Page Size**: 20 items per page
- **Pagination Class**: PageNumberPagination

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`
- **OpenAPI Schema**: `http://127.0.0.1:8000/swagger.json/`

### Postman Collection
Import `Sales_Invoice_API.postman_collection.json` into Postman for:
- Pre-configured API requests
- Environment variables setup
- Automated token management
- Complete API testing workflow

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS` for your domain
3. Set up PostgreSQL database
4. Configure environment variables
5. Set up static file serving
6. Run database migrations
7. Collect static files
8. Set up SSL/HTTPS
9. Configure proper CORS settings

### Environment Variables
Create a `.env` file for production:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add tests for new functionality
- Update documentation for API changes
- Ensure all tests pass before submitting PR



## 🆘 Support & Troubleshooting

### Common Issues
1. **Token Expired**: Use refresh token to get new access token
2. **Permission Denied**: Ensure user is authenticated and has proper permissions
3. **Validation Errors**: Check request data format and required fields
4. **Database Errors**: Run migrations if schema changes were made

### Getting Help
- Check the API documentation at `/swagger/`
- Review the Postman collection for examples
- Create an issue in the repository
- Check Django logs for detailed error messages

## 🔄 Version History

- **v1.0.0** - Initial release
  - Complete invoice management system
  - JWT authentication
  - Transaction tracking
  - API documentation
  - Comprehensive test suite

## 🎯 Future Enhancements

- [ ] Email notifications for invoice status changes
- [ ] PDF invoice generation
- [ ] Advanced reporting and analytics
- [ ] Multi-currency support
- [ ] Invoice templates
- [ ] Customer management system
- [ ] Payment gateway integration

---

