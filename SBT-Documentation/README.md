# Sales By Twilight API

A professional REST API for a grocery store e-commerce platform built with Python, Flask, and MySQL.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.x-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Tests](https://img.shields.io/badge/Tests-95+-brightgreen.svg)

---

## Features

- ✅ **Full CRUD** for all entities (Categories, Products, Customers, Orders)
- ✅ **Consistent JSON response format** across all endpoints
- ✅ **Comprehensive input validation** with meaningful error messages
- ✅ **Filtering and sorting** on list endpoints
- ✅ **Stock management** with automatic inventory tracking
- ✅ **Order lifecycle** with status workflow and business rules
- ✅ **Object-oriented design** with inheritance (BaseModel pattern)
- ✅ **Exception handling** with appropriate HTTP status codes
- ✅ **Unit and integration tests** with pytest
- ✅ **API documentation** with Swagger/OpenAPI

---

## Quick Start

### Prerequisites

- Python 3.12+
- MySQL 8.0+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/sales-by-twilight.git
cd sales-by-twilight

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
mysql -u root < db/schema.sql
mysql -u root < db/seed_data.sql  # Optional: sample data

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run the application
python run.py
```

### Access

- **API**: http://127.0.0.1:5001
- **Documentation**: http://127.0.0.1:5001/api/docs
- **Health Check**: http://127.0.0.1:5001/health

---

## API Endpoints (26 Total)

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories |
| GET | `/categories/<id>` | Get single category |
| POST | `/categories` | Create category |
| PUT | `/categories/<id>` | Update category |
| DELETE | `/categories/<id>` | Delete category |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List products (filter by category, price, stock) |
| GET | `/products/<id>` | Get single product |
| POST | `/products` | Create product |
| PUT | `/products/<id>` | Update product |
| DELETE | `/products/<id>` | Delete product |
| PATCH | `/products/<id>/stock` | Update stock quantity |

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | List customers (filter by name, email) |
| GET | `/customers/<id>` | Get single customer |
| POST | `/customers` | Create customer |
| PUT | `/customers/<id>` | Update customer |
| DELETE | `/customers/<id>` | Delete customer |
| GET | `/customers/<id>/orders` | Get customer's orders |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | List orders (filter by customer, status, date, total) |
| GET | `/orders/<id>` | Get order with items |
| POST | `/orders` | Create order |
| PATCH | `/orders/<id>/status` | Update order status |
| DELETE | `/orders/<id>` | Delete order |
| GET | `/orders/<id>/items` | Get order items |
| POST | `/orders/<id>/items` | Add item to order |
| DELETE | `/orders/<id>/items/<item_id>` | Remove item from order |

---

## Response Format

### Success

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

### Error

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": { ... }
  }
}
```

---

## Examples

### Create a Product

```bash
curl -X POST http://127.0.0.1:5001/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Organic Bananas",
    "price": 1.29,
    "stock_quantity": 100,
    "category_id": 1
  }'
```

### Filter Products

```bash
# By category
curl "http://127.0.0.1:5001/products?category_id=1"

# By price range
curl "http://127.0.0.1:5001/products?min_price=1&max_price=5"

# In stock, sorted by price
curl "http://127.0.0.1:5001/products?in_stock=true&sort=price&order=asc"
```

### Create an Order

```bash
curl -X POST http://127.0.0.1:5001/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 5, "quantity": 1}
    ]
  }'
```

### Update Order Status

```bash
curl -X PATCH http://127.0.0.1:5001/orders/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "processing"}'
```

---

## Project Structure

```
sales-by-twilight/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models/               # Data models with inheritance
│   │   ├── base_model.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── customer.py
│   │   └── order.py
│   ├── routes/               # API endpoints
│   │   ├── category_routes.py
│   │   ├── product_routes.py
│   │   ├── customer_routes.py
│   │   └── order_routes.py
│   └── utils/                # Utilities
│       ├── error_handler.py  # Consistent responses
│       ├── validators.py     # Input validation
│       └── database.py       # DB utilities
├── db/
│   ├── schema.sql
│   └── seed_data.sql
├── tests/
│   ├── test_category.py
│   ├── test_product.py
│   ├── test_integration.py
│   └── test_customer_order_integration.py
├── docs/
├── .env
├── requirements.txt
├── run.py
└── swagger.yaml
```

---

## Business Rules

### Stock Management
- Stock automatically decremented when orders created
- Stock restored when orders cancelled or deleted

### Order Status Workflow
```
pending → processing → shipped → delivered
    ↓         ↓           ↓
    └─────────┴───────────┴──→ cancelled
```

### Constraints
- Cannot delete customers with existing orders
- Cannot delete products that are part of orders
- Cannot modify non-pending orders
- Cannot delete delivered orders
- Email addresses must be unique

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app

# Specific tests
pytest tests/test_integration.py -v
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [API Documentation](docs/API_DOCUMENTATION.md) | Complete endpoint reference |
| [Technical Specification](docs/TECHNICAL_SPEC.md) | Architecture and design |
| [Test Plan](docs/TEST_PLAN.md) | Testing strategy |
| [Setup Guide](docs/SETUP_GUIDE.md) | Installation instructions |

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Framework | Flask 3.0.x |
| Database | MySQL 8.0+ |
| Testing | pytest |
| Documentation | Swagger/OpenAPI |

---

## Author

**Nkem** - Coding Black Females Academy

---

## License

MIT License