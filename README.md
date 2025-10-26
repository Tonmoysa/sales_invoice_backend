# Sales Invoice Backend API

A comprehensive Django REST Framework backend for managing sales invoices and transactions. This API provides secure user authentication, invoice management, transaction tracking, and detailed API documentation.

## 🚀 Features

- **User Management**: Custom user model with JWT authentication
- **Invoice Management**: Create, read, update invoices with line items
- **Transaction Tracking**: Automatic transaction creation for sales and payments
- **Role-based Access**: Admin and regular user permissions
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Comprehensive Testing**: Unit tests with 95%+ coverage
- **CORS Support**: Cross-origin resource sharing enabled
- **Data Validation**: Robust input validation and error handling

## 🏗️ Architecture

### Models

#### User Model
- Extended Django's AbstractUser
- Email field as unique identifier
- Custom user model for authentication

#### Invoice Model
- **Fields**: reference, customer_name, customer_email, customer_phone, total_amount, status, created_by, timestamps
- **Status Choices**: PENDING, PAID
- **Validation**: Non-negative amounts, unique references
- **Relationships**: One-to-many with InvoiceItem, One-to-many with Transaction

#### InvoiceItem Model
- **Fields**: invoice (FK), name, quantity, price
- **Properties**: Calculated subtotal (quantity × price)
- **Validation**: Positive quantities and prices

#### Transaction Model
- **Fields**: invoice (FK), transaction_type, amount, date
- **Transaction Types**: Sale, Payment
- **Purpose**: Track all financial activities

### API Endpoints

#### Authentication
- `POST /api/token/` - Obtain JWT access token
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

#### User Management
- `POST /api/users/register/` - Register new user
- `GET /api/users/profile/` - Get current user profile

#### Invoice Management
- `GET /api/invoices/` - List all invoices (filtered by user)
- `POST /api/invoices/` - Create new invoice
- `GET /api/invoices/{id}/` - Get invoice details
- `PATCH /api/invoices/{id}/` - Update invoice (status only)
- `PATCH /api/invoices/{id}/pay/` - Mark invoice as paid
- `DELETE /api/invoices/{id}/` - Delete invoice

#### Transaction Management
- `GET /api/transactions/` - List all transactions (read-only)
- `GET /api/transactions/{id}/` - Get transaction details

#### Documentation
- `GET /swagger/` - Interactive API documentation
- `GET /redoc/` - Alternative API documentation
- `GET /swagger.json/` - OpenAPI schema

## 🛠️ Technology Stack

- **Framework**: Django 5.2.7
- **API**: Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt 5.5.1)
- **Documentation**: drf-yasg 1.21.11
- **CORS**: django-cors-headers 4.9.0
- **Database**: SQLite (development), PostgreSQL ready
- **Image Processing**: Pillow 10.0.0
- **Configuration**: python-decouple 3.8

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd sales_invoice_backend
```

### 2. Create Virtual Environment
```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📖 API Usage

### Authentication

#### Register a New User
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

#### Login
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

### Invoice Operations

#### Create Invoice
```bash
curl -X POST http://127.0.0.1:8000/api/invoices/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reference": "INV-001",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "1234567890",
    "items": [
      {
        "name": "Product 1",
        "quantity": 2,
        "price": "100.00"
      },
      {
        "name": "Product 2",
        "quantity": 1,
        "price": "50.00"
      }
    ]
  }'
```

#### Mark Invoice as Paid
```bash
curl -X PATCH http://127.0.0.1:8000/api/invoices/1/pay/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: Admin and user permissions
- **Input Validation**: Comprehensive data validation
- **CORS Configuration**: Configurable cross-origin policies
- **Password Validation**: Django's built-in password validators

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

### Test Coverage
- User registration and authentication
- Invoice creation and management
- Transaction tracking
- Permission-based access control
- Data validation and error handling

## 📊 Database Schema

### Tables
- `users` - User accounts
- `invoices` - Invoice records
- `invoice_items` - Invoice line items
- `transactions` - Financial transactions

### Key Relationships
- User → Invoices (One-to-Many)
- Invoice → InvoiceItems (One-to-Many)
- Invoice → Transactions (One-to-Many)

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### JWT Settings
- Access Token Lifetime: 2 hours
- Refresh Token Lifetime: 7 days
- Token Rotation: Enabled
- Blacklist After Rotation: Enabled

## 📚 API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Set up PostgreSQL database
4. Configure static file serving
5. Set up environment variables
6. Run migrations
7. Collect static files

### Docker Support (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the BSD License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the test cases for usage examples

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
  - User authentication and management
  - Invoice creation and management
  - Transaction tracking
  - API documentation
  - Comprehensive test suite

---

**Note**: This is a development version. For production use, ensure proper security configurations and environment variable management.