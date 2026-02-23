# Sales By Twilight API - Technical Specification

## Version 1.0.0

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Database Design](#database-design)
5. [Application Layers](#application-layers)
6. [Error Handling Strategy](#error-handling-strategy)
7. [Input Validation](#input-validation)
8. [Testing Strategy](#testing-strategy)
9. [Configuration Management](#configuration-management)
10. [API Design Principles](#api-design-principles)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│              (Web Browser, Mobile App, Postman, cURL)            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API LAYER                                │
│                     Flask Application                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Category   │  │   Product   │  │  Customer   │             │
│  │   Routes    │  │   Routes    │  │   Routes    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│  ┌─────────────┐                                                │
│  │   Order     │                                                │
│  │   Routes    │                                                │
│  └─────────────┘                                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       UTILITIES LAYER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Error     │  │  Validators │  │  Database   │             │
│  │  Handler    │  │             │  │  Utilities  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        MODEL LAYER                               │
│  ┌─────────────┐                                                │
│  │  BaseModel  │◄─────────────────────────────────┐             │
│  └─────────────┘                                  │             │
│         ▲                                         │ Inheritance │
│         │                                         │             │
│  ┌──────┴──────┬──────────────┬─────────────┐    │             │
│  │  Category   │   Product    │  Customer   │    │             │
│  └─────────────┴──────────────┴─────────────┘    │             │
│  ┌─────────────┬──────────────┐                  │             │
│  │    Order    │  OrderItem   │──────────────────┘             │
│  └─────────────┴──────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                              │
│                         MySQL 8.0+                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ category │  │ product  │  │ customer │  │  order   │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                            ┌──────────┐        │
│                                            │order_item│        │
│                                            └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### Request Flow

```
1. Client sends HTTP request
2. Flask routes request to appropriate Blueprint
3. Route handler validates input using Validators
4. Route handler performs database operations using Database utilities
5. Route handler formats response using Error Handler utilities
6. JSON response returned to client
```

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.12+ | Primary programming language |
| Framework | Flask | 3.0.x | Web framework for REST API |
| Database | MySQL | 8.0+ | Relational data storage |
| DB Driver | mysql-connector-python | 8.3.x | Database connectivity |
| Testing | pytest | 8.0.x | Unit and integration testing |
| Environment | python-dotenv | 1.0.x | Environment variable management |
| Documentation | Swagger/OpenAPI | 3.0 | API documentation |

---

## Project Structure

```
sales-by-twilight/
│
├── app/                              # Main application package
│   ├── __init__.py                  # Flask application factory
│   │
│   ├── models/                      # Data models (OOP with inheritance)
│   │   ├── __init__.py
│   │   ├── base_model.py           # Parent class with common attributes
│   │   ├── category.py             # Category model
│   │   ├── product.py              # Product model
│   │   ├── customer.py             # Customer model
│   │   ├── order.py                # Order model
│   │   └── order_item.py           # OrderItem model
│   │
│   ├── routes/                      # API endpoint handlers
│   │   ├── __init__.py
│   │   ├── category_routes.py      # Category CRUD endpoints
│   │   ├── product_routes.py       # Product CRUD + stock endpoints
│   │   ├── customer_routes.py      # Customer CRUD endpoints
│   │   └── order_routes.py         # Order CRUD + items endpoints
│   │
│   └── utils/                       # Utility modules
│       ├── __init__.py
│       ├── error_handler.py        # Consistent response formatting
│       ├── validators.py           # Input validation
│       └── database.py             # DB connection and query utilities
│
├── db/                              # Database files
│   ├── schema.sql                  # Database schema definition
│   └── seed_data.sql               # Sample data for testing
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_category.py            # Category model unit tests
│   ├── test_product.py             # Product model unit tests
│   ├── test_integration.py         # Category/Product API tests
│   └── test_customer_order_integration.py  # Customer/Order API tests
│
├── docs/                            # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── TECHNICAL_SPEC.md
│   └── ...
│
├── .env                             # Environment variables (not in git)
├── .gitignore                       # Git ignore rules
├── requirements.txt                 # Python dependencies
├── run.py                           # Application entry point
├── swagger.yaml                     # OpenAPI specification
└── README.md                        # Project documentation
```

---

## Database Design

### Entity Relationship Diagram

```
┌─────────────────────┐
│      category       │
├─────────────────────┤
│ PK  id              │
│     name            │
│     description     │
│     created_at      │
│     updated_at      │
└──────────┬──────────┘
           │
           │ 1:N (ON DELETE SET NULL)
           ▼
┌─────────────────────┐         ┌─────────────────────┐
│      product        │         │      customer       │
├─────────────────────┤         ├─────────────────────┤
│ PK  id              │         │ PK  id              │
│     name            │         │     first_name      │
│     description     │         │     last_name       │
│     price           │         │     email (UNIQUE)  │
│     stock_quantity  │         │     phone           │
│ FK  category_id     │         │     created_at      │
│     created_at      │         │     updated_at      │
│     updated_at      │         └──────────┬──────────┘
└──────────┬──────────┘                    │
           │                               │ 1:N (ON DELETE CASCADE)
           │                               ▼
           │                    ┌─────────────────────┐
           │                    │       order         │
           │                    ├─────────────────────┤
           │                    │ PK  id              │
           │                    │ FK  customer_id     │
           │                    │     total_amount    │
           │                    │     status          │
           │                    │     created_at      │
           │                    │     updated_at      │
           │                    └──────────┬──────────┘
           │                               │
           │                               │ 1:N (ON DELETE CASCADE)
           │                               ▼
           │                    ┌─────────────────────┐
           └───────────────────►│     order_item      │
             N:1 (ON DELETE     ├─────────────────────┤
             SET NULL)          │ PK  id              │
                                │ FK  order_id        │
                                │ FK  product_id      │
                                │     quantity        │
                                │     unit_price      │
                                │     created_at      │
                                └─────────────────────┘
```

### Table Specifications

#### category

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Category name |
| description | VARCHAR(500) | NULL | Category description |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

#### product

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(200) | NOT NULL | Product name |
| description | TEXT | NULL | Product description |
| price | DECIMAL(10,2) | NOT NULL | Price in GBP |
| stock_quantity | INT | DEFAULT 0 | Available stock |
| category_id | INT | FOREIGN KEY, ON DELETE SET NULL | Category reference |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

#### customer

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| first_name | VARCHAR(50) | NOT NULL | Customer first name |
| last_name | VARCHAR(50) | NOT NULL | Customer last name |
| email | VARCHAR(100) | NOT NULL, UNIQUE | Email address |
| phone | VARCHAR(20) | NULL | Phone number |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

#### order

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| customer_id | INT | FOREIGN KEY, ON DELETE CASCADE | Customer reference |
| total_amount | DECIMAL(10,2) | NOT NULL | Order total in GBP |
| status | ENUM | NOT NULL, DEFAULT 'pending' | Order status |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Status Values:** `pending`, `processing`, `shipped`, `delivered`, `cancelled`

#### order_item

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| order_id | INT | FOREIGN KEY, ON DELETE CASCADE | Order reference |
| product_id | INT | FOREIGN KEY, ON DELETE SET NULL | Product reference |
| quantity | INT | NOT NULL | Quantity ordered |
| unit_price | DECIMAL(10,2) | NOT NULL | Price at time of order |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

---

## Application Layers

### 1. Routes Layer (app/routes/)

Handles HTTP requests and responses. Each entity has its own Blueprint.

**Responsibilities:**
- Parse request parameters and body
- Call validators for input validation
- Perform database operations
- Format and return responses

**Pattern:**
```python
@blueprint.route('/endpoint', methods=['GET'])
@handle_exceptions  # Decorator for consistent error handling
def endpoint_handler():
    # 1. Parse input
    # 2. Validate input
    # 3. Database operations
    # 4. Return response
```

### 2. Utilities Layer (app/utils/)

Provides shared functionality across the application.

#### error_handler.py

| Component | Purpose |
|-----------|---------|
| `APIError` | Custom exception class |
| `error_response()` | Create consistent error responses |
| `success_response()` | Create consistent success responses |
| `handle_exceptions` | Decorator for route exception handling |
| `Errors` | Predefined error responses |

#### validators.py

| Component | Purpose |
|-----------|---------|
| `Validator` | Fluent validation builder |
| `validate_*_create()` | Entity creation validators |
| `validate_*_update()` | Entity update validators |

#### database.py

| Component | Purpose |
|-----------|---------|
| `get_db_connection()` | Create database connection |
| `get_db_cursor()` | Context manager for cursor operations |
| `QueryBuilder` | Dynamic SQL query builder |
| `row_exists()` | Check if record exists |
| `get_row_by_id()` | Fetch single record |

### 3. Model Layer (app/models/)

Data classes representing database entities with inheritance.

```python
class BaseModel:
    # Common attributes: id, created_at, updated_at
    # Common methods: to_dict(), __repr__()

class Category(BaseModel):
    # Category-specific: name, description

class Product(BaseModel):
    # Product-specific: name, description, price, stock_quantity, category_id

class Customer(BaseModel):
    # Customer-specific: first_name, last_name, email, phone

class Order(BaseModel):
    # Order-specific: customer_id, total_amount, status

class OrderItem(BaseModel):
    # OrderItem-specific: order_id, product_id, quantity, unit_price
```

---

## Error Handling Strategy

### Exception Handling Flow

```
Route Handler
     │
     ├─► Input Validation Error
     │         │
     │         └─► Return 400 with VALIDATION_ERROR
     │
     ├─► Resource Not Found
     │         │
     │         └─► Return 404 with RESOURCE_NOT_FOUND
     │
     ├─► Business Rule Violation
     │         │
     │         └─► Return 400/409 with specific error code
     │
     ├─► Database Error
     │         │
     │         └─► Return 500 with DATABASE_ERROR
     │
     └─► Unexpected Error
               │
               └─► Return 500 with INTERNAL_ERROR
```

### Response Format

All errors follow the same structure:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": {}  // Optional additional information
  }
}
```

---

## Input Validation

### Validation Rules by Entity

#### Category

| Field | Rules |
|-------|-------|
| name | Required, string, max 100 chars, not empty |
| description | Optional, string, max 500 chars |

#### Product

| Field | Rules |
|-------|-------|
| name | Required, string, max 200 chars, not empty |
| description | Optional, string, max 1000 chars |
| price | Required, positive decimal |
| stock_quantity | Optional, non-negative integer, default 0 |
| category_id | Optional, positive integer, must exist |

#### Customer

| Field | Rules |
|-------|-------|
| first_name | Required, string, max 50 chars |
| last_name | Required, string, max 50 chars |
| email | Required, valid email format, unique, max 100 chars |
| phone | Optional, valid phone format, max 20 chars |

#### Order

| Field | Rules |
|-------|-------|
| customer_id | Required, positive integer, must exist |
| items | Required, non-empty array |
| items[].product_id | Required, positive integer, must exist |
| items[].quantity | Required, positive integer |

---

## Testing Strategy

### Test Categories

| Type | Location | Purpose |
|------|----------|---------|
| Unit Tests | tests/test_*.py (models) | Test model classes in isolation |
| Integration Tests | tests/test_*_integration.py | Test API endpoints end-to-end |

### Test Coverage Goals

| Entity | Unit Tests | Integration Tests |
|--------|------------|-------------------|
| Category | Model attributes, inheritance | CRUD operations, filtering |
| Product | Model attributes | CRUD, filtering, stock management |
| Customer | Model attributes | CRUD, email uniqueness, orders |
| Order | Model attributes | Full lifecycle, items, status workflow |

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_integration.py -v

# With coverage
pytest tests/ -v --cov=app
```

---

## Configuration Management

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | Database server address |
| `DB_PORT` | 3306 | Database server port |
| `DB_NAME` | sales_by_twilight | Database name |
| `DB_USER` | root | Database username |
| `DB_PASSWORD` | (empty) | Database password |
| `FLASK_ENV` | development | Environment mode |
| `FLASK_DEBUG` | true | Enable debug mode |
| `SECRET_KEY` | (generated) | Flask secret key |

### .env File Example

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=sales_by_twilight
DB_USER=root
DB_PASSWORD=your_password
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=your-secret-key-here
```

---

## API Design Principles

### RESTful Conventions

| Principle | Implementation |
|-----------|----------------|
| Resource-based URLs | `/categories`, `/products`, `/customers`, `/orders` |
| HTTP methods for actions | GET (read), POST (create), PUT (update), DELETE (remove), PATCH (partial update) |
| Plural nouns | `/categories` not `/category` |
| Hierarchical resources | `/orders/{id}/items`, `/customers/{id}/orders` |
| Query params for filtering | `?category_id=1&min_price=5` |
| Consistent response format | `{success, data, error, message}` |

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Files | snake_case | `category_routes.py` |
| Classes | PascalCase | `BaseModel`, `Category` |
| Functions | snake_case | `get_all_categories()` |
| Variables | snake_case | `category_id` |
| Constants | UPPER_SNAKE | `ORDER_STATUSES` |
| URL paths | kebab-case (lowercase) | `/order-items` |
| JSON keys | snake_case | `created_at`, `stock_quantity` |
