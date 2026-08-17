# Farm Food Delivery API Backend

A complete, lightweight REST API backend for a rural/farm food delivery iOS application. This MVP focuses on simplicity and ease of maintenance, designed for a business model where farmers are not direct users of the application.

## Business Model

**Flow:** Farmers → Business Owner → iOS App → Customer → Delivery

- **Farmers:** Supply products directly to the business owner
- **Business Owner/Admin:** Manages products, categories, and orders through admin panel
- **Customers:** Browse products, add to local cart on mobile, place orders, receive deliveries
- **No farmer accounts or farmer dashboard** - all product management is done by the admin

## Features

### Customer Features
- **Authentication:** Phone number-based registration and login with user_id parameter
- **Products:** Browse, search, and filter products by category
- **Categories:** View product categories and their products
- **Local Cart:** Cart is managed locally on the mobile app for better performance
- **Addresses:** Save and manage delivery addresses
- **Orders:** Place orders directly with items, view order history, cancel orders (when allowed)
- **Payment:** Cash on delivery (MVP)

### Admin Features
- **Authentication:** Admin login with admin_id parameter
- **Product Management:** Create, update, delete products, manage stock and availability
- **Category Management:** Create, update, delete categories
- **Order Management:** View all orders, update order status

### Technical Features
- **Security:** Parameter-based authentication, password hashing, input validation, CORS
- **Database:** SQLAlchemy ORM with PostgreSQL (SQLite for development)
- **Migrations:** Flask-Migrate for database schema management
- **Testing:** Basic test suite for all endpoints
- **API Response Format:** Consistent JSON responses
- **Simplified Order Flow:** Orders are created directly with items (no server-side cart)

## Technology Stack

- **Python 3.12+**
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-Migrate 4.0.5** - Database migrations
- **Flask-CORS 4.0.0** - CORS support
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **pytest** - Testing framework

## Project Structure

```
backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration classes
│   ├── extensions.py            # Flask extensions
│   ├── models/                  # Database models
│   │   ├── user.py             # Customer model
│   │   ├── admin.py            # Admin model
│   │   ├── category.py         # Category model
│   │   ├── product.py          # Product model
│   │   ├── address.py          # Address model
│   │   ├── order.py            # Order model
│   │   └── order_item.py       # Order item model
│   ├── routes/                  # API routes (blueprints)
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── products.py         # Product endpoints
│   │   ├── categories.py       # Category endpoints
│   │   ├── addresses.py        # Address endpoints
│   │   ├── orders.py           # Order endpoints
│   │   └── admin.py            # Admin endpoints
│   ├── services/                # Business logic layer
│   │   ├── order_service.py    # Order operations
│   │   └── product_service.py  # Product operations
│   └── utils/                   # Utility functions
│       └── responses.py        # Response helpers
├── migrations/                  # Database migration files
├── tests/                       # Test files
│   ├── __init__.py
│   └── test_api.py             # API tests
├── .env                         # Environment variables (not in git)
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- PostgreSQL (for production)

### Setup

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-change-in-production
   DATABASE_URL=sqlite:///farm_delivery.db
   JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
   DELIVERY_FEE=30
   CORS_ORIGINS=*
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the server**
   ```bash
   python run.py
   ```

   The server will start on `http://localhost:5000`

## Database Setup

### Development (SQLite)
The default configuration uses SQLite for development. No additional setup required.

### Production (PostgreSQL)

1. **Install PostgreSQL**
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt-get install postgresql
   sudo service postgresql start
   ```

2. **Create database**
   ```bash
   createdb farm_delivery
   ```

3. **Update .env file**
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/farm_delivery
   ```

4. **Run migrations**
   ```bash
   flask db upgrade
   ```

## API Endpoints

### Authentication (Customer)

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "phone": "1234567890",
  "password": "password123",
  "confirm_password": "password123"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "phone": "1234567890",
  "password": "password123"
}
```

**Note:** Login returns user_id which must be used as a parameter in subsequent requests.

#### Get Current User
```http
GET /api/auth/me?user_id=1
```

### Addresses

#### Get Addresses
```http
GET /api/addresses?user_id=1
```

#### Create Address
```http
POST /api/addresses?user_id=1
Content-Type: application/json

{
  "title": "Home",
  "full_address": "123 Main Street",
  "city": "Cairo",
  "area": "Downtown",
  "phone": "1234567890",
  "latitude": 30.0444,
  "longitude": 31.2357,
  "is_default": true
}
```

#### Update Address
```http
PUT /api/addresses/{id}?user_id=1
Content-Type: application/json

{
  "title": "Work",
  "full_address": "456 Business Ave"
}
```

#### Delete Address
```http
DELETE /api/addresses/{id}?user_id=1
```

### Products

#### Get Products
```http
GET /api/products?search=cheese&category_id=1&page=1&per_page=20
```

#### Get Product Details
```http
GET /api/products/{id}
```

### Categories

#### Get Categories
```http
GET /api/categories
```

#### Get Category Products
```http
GET /api/categories/{id}/products
```

### Addresses

#### Get Addresses
```http
GET /api/addresses
Authorization: Bearer <access_token>
```

#### Create Address
```http
POST /api/addresses
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Home",
  "full_address": "123 Main Street",
  "city": "Cairo",
  "area": "Downtown",
  "phone": "1234567890",
  "latitude": 30.0444,
  "longitude": 31.2357,
  "is_default": true
}
```

#### Update Address
```http
PUT /api/addresses/{id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Work",
  "full_address": "456 Business Ave"
}
```

#### Delete Address
```http
DELETE /api/addresses/{id}
Authorization: Bearer <access_token>
```

### Orders

#### Get Orders
```http
GET /api/orders?user_id=1&page=1&per_page=20
```

#### Get Order Details
```http
GET /api/orders/{id}?user_id=1
```

#### Create Order
```http
POST /api/orders?user_id=1
Content-Type: application/json

{
  "address_id": 1,
  "payment_method": "cash_on_delivery",
  "notes": "Please call before delivery",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

#### Cancel Order
```http
POST /api/orders/{id}/cancel?user_id=1
```

### Admin

#### Admin Login
```http
POST /api/admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Note:** Admin login returns admin_id which must be used as a parameter in subsequent requests.

#### Create Product
```http
POST /api/admin/products?admin_id=1
Content-Type: application/json

{
  "name": "Fresh Milk",
  "description": "Fresh farm milk",
  "price": 50.00,
  "unit": "liter",
  "category_id": 1,
  "available_quantity": 100,
  "is_available": true,
  "image_url": "https://example.com/milk.jpg"
}
```

#### Update Product
```http
PUT /api/admin/products/{id}?admin_id=1
Content-Type: application/json

{
  "name": "Fresh Milk",
  "price": 55.00,
  "available_quantity": 80
}
```

#### Delete Product
```http
DELETE /api/admin/products/{id}?admin_id=1
```

#### Update Product Stock
```http
PATCH /api/admin/products/{id}/stock?admin_id=1
Content-Type: application/json

{
  "quantity": 50
}
```

#### Update Product Availability
```http
PATCH /api/admin/products/{id}/availability?admin_id=1
Content-Type: application/json

{
  "is_available": false
}
```

#### Create Category
```http
POST /api/admin/categories?admin_id=1
Content-Type: application/json

{
  "name": "Dairy",
  "image_url": "https://example.com/dairy.jpg"
}
```

#### Update Category
```http
PUT /api/admin/categories/{id}?admin_id=1
Content-Type: application/json

{
  "name": "Dairy Products"
}
```

#### Delete Category
```http
DELETE /api/admin/categories/{id}?admin_id=1
```

#### Get All Orders
```http
GET /api/admin/orders?admin_id=1&page=1&per_page=20&status=pending
```

#### Get Order Details
```http
GET /api/admin/orders/{id}?admin_id=1
```

#### Update Order Status
```http
PATCH /api/admin/orders/{id}/status?admin_id=1
Content-Type: application/json

{
  "status": "confirmed"
}
```

Valid order statuses: `pending`, `confirmed`, `preparing`, `out_for_delivery`, `delivered`, `cancelled`

## API Response Format

### Success Response
```json
{
  "success": true,
  "message": "Success message",
  "data": {
    // Response data
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "data": null
}
```

## Security Features

- **Parameter-Based Authentication:** Simple user_id/admin_id parameter authentication
- **Password Hashing:** Passwords are securely hashed using Werkzeug
- **Input Validation:** All inputs are validated before processing
- **CORS:** Configurable CORS for cross-origin requests
- **Environment Variables:** Sensitive data stored in environment variables
- **Price Protection:** Backend calculates all prices; client cannot manipulate totals
- **Ownership Validation:** Customers can only access their own data based on user_id
- **Authorization:** Separate authentication for customers and admins

## Testing

Run the test suite:
```bash
pytest tests/test_api.py -v
```

Run with coverage:
```bash
pytest tests/test_api.py --cov=app --cov-report=html
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_APP` | Flask application entry point | `run.py` |
| `FLASK_ENV` | Environment (development/production) | `development` |
| `SECRET_KEY` | Flask secret key for sessions | (dev key) |
| `DATABASE_URL` | Database connection string | `sqlite:///farm_delivery.db` |
| `DELIVERY_FEE` | Default delivery fee | `30` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |

### Delivery Fee

The delivery fee is configurable via the `DELIVERY_FEE` environment variable. For the MVP, a flat fee is used. Future versions can implement delivery zones with different fees.

## Order Status Flow

```
pending → confirmed → preparing → out_for_delivery → delivered
                   ↘ cancelled ↙
```

Customers can only cancel orders in `pending` or `confirmed` status.

## Inventory Management

- Stock is automatically decreased when orders are created
- Stock is restored when orders are cancelled (before preparation)
- Stock cannot go negative
- All inventory operations use database transactions

## Deployment

### Production Setup

1. **Use PostgreSQL**
   ```env
   DATABASE_URL=postgresql://user:password@host:5432/farm_delivery
   ```

2. **Set strong secret keys**
   ```env
   SECRET_KEY=your-strong-secret-key
   JWT_SECRET_KEY=your-strong-jwt-key
   ```

3. **Configure CORS**
   ```env
   CORS_ORIGINS=https://your-ios-app-domain.com
   ```

4. **Set environment to production**
   ```env
   FLASK_ENV=production
   ```

5. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

## Development Notes

### Adding the First Admin

Since there's no admin registration endpoint, you'll need to create the first admin manually:

```python
from app import create_app
from app.extensions import db
from app.models.admin import Admin

app = create_app()
with app.app_context():
    admin = Admin(username='admin')
    admin.set_password('your-secure-password')
    db.session.add(admin)
    db.session.commit()
    print('Admin created successfully')
```

### iOS App Integration Notes

**Important Authentication Method:**

1. **Authentication:** Use user_id/admin_id as URL parameters
   - Login/Register returns user information including user_id
   - Include user_id as a parameter in all subsequent requests
   - Example: `GET /api/addresses?user_id=1`
   - Admin endpoints use admin_id parameter similarly

2. **Local Cart Management:** 
   - Cart is managed locally on the iOS app
   - When placing an order, send the cart items directly in the request
   - Server validates products, calculates prices, and checks stock

3. **Order Creation:**
   - Send items array directly with order creation
   - Backend handles all price calculations and validation
   - Example order payload:
   ```json
   {
     "address_id": 1,
     "payment_method": "cash_on_delivery",
     "notes": "Please call before delivery",
     "items": [
       {"product_id": 1, "quantity": 2},
       {"product_id": 3, "quantity": 1}
     ]
   }
   ```

### Database Migrations

When you modify models:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

To rollback:
```bash
flask db downgrade
```

## Future Enhancements (Not in MVP)

- Payment gateway integration
- OTP for phone verification
- Social login
- Reviews and ratings
- Favorites/wishlist
- Push notifications
- Redis for caching
- Live delivery tracking
- Delivery zones with variable fees
- Email notifications
- Image upload with cloud storage
- Server-side cart synchronization (optional)

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `createdb farm_delivery`

### Migration Issues
- Delete migrations folder and run `flask db init` again
- Or use `flask db stamp head` to mark current state

### JWT Token Issues
- Ensure JWT_SECRET_KEY is set in .env
- Check token expiration (default 24 hours)

### CORS Issues
- Check CORS_ORIGINS in .env
- Ensure your iOS app domain is included

## License

This project is proprietary software. All rights reserved.

## Support

For issues and questions, please contact the development team.
