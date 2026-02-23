# Sales By Twilight API Documentation

## Version 1.0.0

Complete REST API reference for the Sales By Twilight grocery store e-commerce platform.

---

## Table of Contents

1. [Overview](#overview)
2. [Base URL](#base-url)
3. [Response Format](#response-format)
4. [HTTP Status Codes](#http-status-codes)
5. [Error Codes](#error-codes)
6. [Categories](#categories)
7. [Products](#products)
8. [Customers](#customers)
9. [Orders](#orders)
10. [Testing Examples](#testing-examples)

---

## Overview

The Sales By Twilight API is a RESTful API that provides endpoints for managing a grocery store e-commerce platform. It supports full CRUD operations for categories, products, customers, and orders.

### Features

- Consistent JSON response format
- Comprehensive input validation
- Filtering and sorting on list endpoints
- Stock management with automatic inventory updates
- Order status workflow with business rules
- Proper error handling with meaningful error codes

---

## Base URL

```
Development: http://127.0.0.1:5001
Production:  https://api.salesbytwilight.com (example)
```

---

## Response Format

All API responses follow a consistent JSON structure.

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... }
  }
}
```

---

## HTTP Status Codes

| Code | Name | Usage |
|------|------|-------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Successful POST (resource created) |
| 400 | Bad Request | Invalid input, validation error |
| 404 | Not Found | Resource does not exist |
| 405 | Method Not Allowed | HTTP method not supported |
| 409 | Conflict | Duplicate entry, resource in use |
| 500 | Internal Server Error | Unexpected server error |

---

## Error Codes

| Code | Description |
|------|-------------|
| `BAD_REQUEST` | Generic bad request |
| `VALIDATION_ERROR` | Input validation failed |
| `MISSING_FIELD` | Required field not provided |
| `INVALID_TYPE` | Field has wrong data type |
| `INVALID_JSON` | Request body is not valid JSON |
| `RESOURCE_NOT_FOUND` | Requested resource does not exist |
| `DUPLICATE_ENTRY` | Record already exists |
| `DUPLICATE_EMAIL` | Email address already registered |
| `INVALID_CATEGORY` | Referenced category does not exist |
| `PRODUCT_IN_USE` | Product is part of existing orders |
| `CUSTOMER_HAS_ORDERS` | Customer has existing orders |
| `INSUFFICIENT_STOCK` | Not enough stock available |
| `INVALID_STATUS` | Invalid order status value |
| `INVALID_STATUS_TRANSITION` | Cannot transition between statuses |
| `ORDER_NOT_MODIFIABLE` | Order cannot be modified |
| `CANNOT_DELETE_DELIVERED` | Delivered orders cannot be deleted |
| `LAST_ITEM_IN_ORDER` | Cannot remove last item from order |
| `DATABASE_ERROR` | Database operation failed |
| `INTERNAL_ERROR` | Unexpected server error |

---

## Categories

Manage product categories for the grocery store.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories |
| GET | `/categories/<id>` | Get single category |
| POST | `/categories` | Create category |
| PUT | `/categories/<id>` | Update category |
| DELETE | `/categories/<id>` | Delete category |

### Category Object

```json
{
  "id": 1,
  "name": "Fresh Produce",
  "description": "Fresh fruits and vegetables",
  "created_at": "2026-02-23T06:42:01",
  "updated_at": "2026-02-23T06:42:01"
}
```

### GET /categories

Retrieve all categories with optional filtering.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| name | string | Filter by name (partial match) |
| sort | string | Sort field: `id`, `name`, `created_at`, `updated_at` |
| order | string | Sort order: `asc`, `desc` |
| limit | integer | Maximum results to return |
| offset | integer | Number of results to skip |

**Example Request:**
```bash
curl "http://127.0.0.1:5001/categories?name=produce&sort=name&order=asc"
```

**Example Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Fresh Produce",
      "description": "Fresh fruits and vegetables",
      "created_at": "2026-02-23T06:42:01",
      "updated_at": "2026-02-23T06:42:01"
    }
  ]
}
```

### GET /categories/{id}

Retrieve a single category by ID.

**Example Request:**
```bash
curl http://127.0.0.1:5001/categories/1
```

**Example Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Fresh Produce",
    "description": "Fresh fruits and vegetables",
    "created_at": "2026-02-23T06:42:01",
    "updated_at": "2026-02-23T06:42:01"
  }
}
```

**Example Response (404):**
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Category with ID 999 not found"
  }
}
```

### POST /categories

Create a new category.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Category name (max 100 chars) |
| description | string | No | Category description (max 500 chars) |

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5001/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Bakery", "description": "Fresh bread and pastries"}'
```

**Example Response (201):**
```json
{
  "success": true,
  "data": {
    "id": 11,
    "name": "Bakery",
    "description": "Fresh bread and pastries",
    "created_at": "2026-02-23T10:30:00",
    "updated_at": "2026-02-23T10:30:00"
  },
  "message": "Category created successfully"
}
```

### PUT /categories/{id}

Update an existing category.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | No | New category name |
| description | string | No | New category description |

At least one field must be provided.

**Example Request:**
```bash
curl -X PUT http://127.0.0.1:5001/categories/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Fresh Produce & Vegetables"}'
```

### DELETE /categories/{id}

Delete a category. Products in this category will have their `category_id` set to NULL.

**Example Request:**
```bash
curl -X DELETE http://127.0.0.1:5001/categories/11
```

---

## Products

Manage products in the grocery store catalogue.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List all products |
| GET | `/products/<id>` | Get single product |
| POST | `/products` | Create product |
| PUT | `/products/<id>` | Update product |
| DELETE | `/products/<id>` | Delete product |
| PATCH | `/products/<id>/stock` | Update stock quantity |

### Product Object

```json
{
  "id": 1,
  "name": "Organic Bananas",
  "description": "Bundle of 5-6 organic bananas",
  "price": 1.29,
  "stock_quantity": 150,
  "category_id": 1,
  "category_name": "Fresh Produce",
  "created_at": "2026-02-23T08:00:00",
  "updated_at": "2026-02-23T08:00:00"
}
```

### GET /products

Retrieve all products with optional filtering.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| category_id | integer | Filter by category |
| name | string | Filter by name (partial match) |
| min_price | float | Minimum price filter |
| max_price | float | Maximum price filter |
| in_stock | boolean | If `true`, only products with stock > 0 |
| sort | string | Sort field: `id`, `name`, `price`, `stock_quantity`, `created_at` |
| order | string | Sort order: `asc`, `desc` |
| limit | integer | Maximum results to return |
| offset | integer | Number of results to skip |

**Example Requests:**
```bash
# Filter by category
curl "http://127.0.0.1:5001/products?category_id=1"

# Filter by price range
curl "http://127.0.0.1:5001/products?min_price=1&max_price=5"

# Only in-stock products sorted by price
curl "http://127.0.0.1:5001/products?in_stock=true&sort=price&order=asc"
```

### POST /products

Create a new product.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Product name (max 200 chars) |
| description | string | No | Product description |
| price | float | Yes | Price in GBP (must be > 0) |
| stock_quantity | integer | No | Initial stock (default 0, must be >= 0) |
| category_id | integer | No | Category ID |

### PATCH /products/{id}/stock

Update product stock quantity.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| quantity | integer | Yes | Stock quantity or adjustment amount |
| operation | string | No | `set`, `add`, or `subtract` (default: `set`) |

**Example Requests:**
```bash
# Set absolute stock
curl -X PATCH http://127.0.0.1:5001/products/1/stock \
  -H "Content-Type: application/json" \
  -d '{"quantity": 100}'

# Add to stock
curl -X PATCH http://127.0.0.1:5001/products/1/stock \
  -H "Content-Type: application/json" \
  -d '{"quantity": 50, "operation": "add"}'
```

---

## Customers

Manage customer accounts.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | List all customers |
| GET | `/customers/<id>` | Get single customer |
| POST | `/customers` | Create customer |
| PUT | `/customers/<id>` | Update customer |
| DELETE | `/customers/<id>` | Delete customer |
| GET | `/customers/<id>/orders` | Get customer's orders |

### Customer Object

```json
{
  "id": 1,
  "first_name": "Emma",
  "last_name": "Thompson",
  "email": "emma.thompson@email.co.uk",
  "phone": "07700900001",
  "created_at": "2026-02-23T09:00:00",
  "updated_at": "2026-02-23T09:00:00"
}
```

### GET /customers

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| email | string | Filter by email (exact match) |
| name | string | Filter by first or last name (partial match) |
| sort | string | Sort field: `id`, `first_name`, `last_name`, `email`, `created_at` |
| order | string | Sort order: `asc`, `desc` |

### GET /customers/{id}

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| include_orders | boolean | If `true`, include customer's orders |

### POST /customers

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| first_name | string | Yes | First name (max 50 chars) |
| last_name | string | Yes | Last name (max 50 chars) |
| email | string | Yes | Email address (must be unique) |
| phone | string | No | Phone number |

### DELETE /customers/{id}

Cannot delete customers with existing orders.

---

## Orders

Manage customer orders with full lifecycle support.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | List all orders |
| GET | `/orders/<id>` | Get single order with items |
| POST | `/orders` | Create order |
| PATCH | `/orders/<id>/status` | Update order status |
| DELETE | `/orders/<id>` | Delete order |
| GET | `/orders/<id>/items` | Get order items |
| POST | `/orders/<id>/items` | Add item to order |
| DELETE | `/orders/<id>/items/<item_id>` | Remove item from order |

### Order Object

```json
{
  "id": 1,
  "customer_id": 1,
  "customer_first_name": "Emma",
  "customer_last_name": "Thompson",
  "customer_email": "emma.thompson@email.co.uk",
  "total_amount": 23.45,
  "status": "pending",
  "created_at": "2026-02-23T10:00:00",
  "updated_at": "2026-02-23T10:00:00",
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Organic Bananas",
      "quantity": 2,
      "unit_price": 1.29,
      "subtotal": 2.58
    }
  ],
  "item_count": 1
}
```

### Order Status Values

| Status | Description |
|--------|-------------|
| `pending` | Order placed, awaiting processing |
| `processing` | Order being prepared |
| `shipped` | Order dispatched for delivery |
| `delivered` | Order delivered to customer |
| `cancelled` | Order cancelled |

### Order Status Transitions

```
pending → processing → shipped → delivered
    ↓         ↓           ↓
    └─────────┴───────────┴──→ cancelled
```

### GET /orders

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Filter by customer |
| status | string | Filter by status |
| min_total | float | Minimum order total |
| max_total | float | Maximum order total |
| date_from | string | Orders after date (YYYY-MM-DD) |
| date_to | string | Orders before date (YYYY-MM-DD) |
| sort | string | Sort field: `id`, `total_amount`, `status`, `created_at` |
| order | string | Sort order: `asc`, `desc` (default: `desc`) |

### POST /orders

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| customer_id | integer | Yes | Customer ID |
| items | array | Yes | Array of order items |
| items[].product_id | integer | Yes | Product ID |
| items[].quantity | integer | Yes | Quantity (must be > 0) |

**Business Rules:**
- Stock is automatically decremented for each item
- Total amount is calculated from current product prices
- Order status is set to `pending`

### PATCH /orders/{id}/status

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | Yes | New status value |

**Business Rules:**
- Must follow valid status transitions
- Cancelling restores product stock
- Cannot change delivered or cancelled orders

### POST /orders/{id}/items

**Business Rules:**
- Can only add items to pending orders
- Stock is automatically decremented
- Order total is recalculated

### DELETE /orders/{id}/items/{item_id}

**Business Rules:**
- Can only remove items from pending orders
- Cannot remove the last item (delete order instead)
- Stock is automatically restored

---

## Appendix: All Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/categories` | List categories |
| GET | `/categories/<id>` | Get category |
| POST | `/categories` | Create category |
| PUT | `/categories/<id>` | Update category |
| DELETE | `/categories/<id>` | Delete category |
| GET | `/products` | List products |
| GET | `/products/<id>` | Get product |
| POST | `/products` | Create product |
| PUT | `/products/<id>` | Update product |
| DELETE | `/products/<id>` | Delete product |
| PATCH | `/products/<id>/stock` | Update stock |
| GET | `/customers` | List customers |
| GET | `/customers/<id>` | Get customer |
| POST | `/customers` | Create customer |
| PUT | `/customers/<id>` | Update customer |
| DELETE | `/customers/<id>` | Delete customer |
| GET | `/customers/<id>/orders` | Get customer orders |
| GET | `/orders` | List orders |
| GET | `/orders/<id>` | Get order |
| POST | `/orders` | Create order |
| PATCH | `/orders/<id>/status` | Update status |
| DELETE | `/orders/<id>` | Delete order |
| GET | `/orders/<id>/items` | Get order items |
| POST | `/orders/<id>/items` | Add item |
| DELETE | `/orders/<id>/items/<item_id>` | Remove item |

**Total: 26 endpoints**
