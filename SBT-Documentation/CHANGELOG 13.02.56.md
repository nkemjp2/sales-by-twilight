# Changelog

All notable changes to the Sales By Twilight API project.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2026-02-23

### Added

#### Core Features
- Full CRUD operations for all entities (Category, Product, Customer, Order)
- Consistent JSON response format across all endpoints
- Comprehensive input validation with meaningful error messages
- Filtering and sorting on all list endpoints
- Pagination support with limit and offset parameters

#### Category Endpoints
- GET /categories - List all categories with name filtering
- GET /categories/{id} - Get single category
- POST /categories - Create category with validation
- PUT /categories/{id} - Update category
- DELETE /categories/{id} - Delete category

#### Product Endpoints
- GET /products - List products with filtering (category, price range, stock)
- GET /products/{id} - Get product with category information
- POST /products - Create product with validation
- PUT /products/{id} - Update product
- DELETE /products/{id} - Delete product (with order protection)
- PATCH /products/{id}/stock - Stock management (set, add, subtract)

#### Customer Endpoints
- GET /customers - List customers with name/email filtering
- GET /customers/{id} - Get customer (optionally include orders)
- POST /customers - Create customer with email uniqueness
- PUT /customers/{id} - Update customer
- DELETE /customers/{id} - Delete customer (with order protection)
- GET /customers/{id}/orders - Get customer's order history

#### Order Endpoints
- GET /orders - List orders with comprehensive filtering
- GET /orders/{id} - Get order with items and customer info
- POST /orders - Create order with automatic stock decrement
- PATCH /orders/{id}/status - Status workflow with validation
- DELETE /orders/{id} - Delete order with stock restoration
- GET /orders/{id}/items - Get order items
- POST /orders/{id}/items - Add item to pending order
- DELETE /orders/{id}/items/{item_id} - Remove item from pending order

#### Utilities Layer
- error_handler.py - Consistent error/success responses
- validators.py - Fluent validation with type checking
- database.py - Connection management and QueryBuilder

#### Business Rules
- Stock automatically decremented on order creation
- Stock restored on order cancellation/deletion
- Valid order status transitions enforced
- Email uniqueness for customers
- Protection against deleting referenced records

#### Testing
- Unit tests for model classes (19+ tests)
- Integration tests for all endpoints (75+ tests)
- Business rule validation tests
- Response format consistency tests

#### Documentation
- API Documentation with all 26 endpoints
- Technical Specification with architecture
- Test Plan with coverage matrix
- Setup Guide with installation steps
- Swagger/OpenAPI specification

---

## [0.2.0] - 2026-02-23

### Added
- Unit tests for Category model (19 tests)
- Comprehensive project documentation
- Demo preparation guide
- Seed data with UK grocery products

### Changed
- Updated README with assessment requirements

---

## [0.1.0] - 2026-02-23

### Added
- Initial project setup
- Flask application factory pattern
- Category model with BaseModel inheritance
- Category GET endpoints (list and single)
- MySQL database schema
- Basic exception handling
- Git repository initialization

---

## Upcoming Features

### [1.1.0] - Planned
- Pagination metadata (total count, pages)
- Search across multiple fields
- Bulk operations
- Export to CSV/Excel

### [1.2.0] - Planned
- JWT authentication
- Role-based access control
- Rate limiting

### [1.3.0] - Planned
- Product images
- Category hierarchy
- Discount/coupon system

### [2.0.0] - Future
- Payment integration
- Shipping integration
- Email notifications
- Admin dashboard
