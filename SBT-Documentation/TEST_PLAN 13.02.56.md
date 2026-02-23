# Sales By Twilight API - Test Plan

## Version 1.0.0

---

## Table of Contents

1. [Test Overview](#test-overview)
2. [Test Environment](#test-environment)
3. [Test Categories](#test-categories)
4. [Unit Tests](#unit-tests)
5. [Integration Tests](#integration-tests)
6. [Test Execution](#test-execution)
7. [Test Coverage Matrix](#test-coverage-matrix)

---

## Test Overview

### Testing Philosophy

- **Unit Tests**: Test individual model classes in isolation
- **Integration Tests**: Test complete API request/response cycles
- **Business Logic Tests**: Verify business rules are enforced

### Test Framework

- **pytest**: Primary testing framework
- **Flask Test Client**: For HTTP request simulation
- **Fixtures**: Reusable test data and setup

---

## Test Environment

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-cov

# Ensure database is running
mysql -u root -e "SELECT 1"

# Ensure test database has schema
mysql -u root < db/schema.sql
```

### Configuration

Tests use the same `.env` configuration as development. Ensure database credentials are correct.

---

## Test Categories

| Category | Purpose | Location |
|----------|---------|----------|
| Unit Tests - Models | Test model classes | `tests/test_category.py`, `tests/test_product.py` |
| Integration Tests | Test API endpoints | `tests/test_integration.py`, `tests/test_customer_order_integration.py` |

---

## Unit Tests

### Category Model Tests (19 tests)

**File:** `tests/test_category.py`

#### TestCategoryInheritance (2 tests)

| Test | Description | Expected |
|------|-------------|----------|
| `test_category_inherits_from_base_model` | Verify Category is subclass of BaseModel | `issubclass(Category, BaseModel) == True` |
| `test_category_instance_is_base_model_instance` | Verify instance type | `isinstance(category, BaseModel) == True` |

#### TestCategoryInstantiation (2 tests)

| Test | Description | Expected |
|------|-------------|----------|
| `test_category_instantiation_with_no_args` | Create with defaults | All attributes None/default |
| `test_category_instantiation_with_all_args` | Create with values | All attributes set correctly |

#### TestCategoryAttributes (5 tests)

| Test | Description | Expected |
|------|-------------|----------|
| `test_category_name_attribute` | Name is set | `category.name == "Test"` |
| `test_category_description_attribute` | Description is set | `category.description == "Desc"` |
| `test_category_id_inherited` | ID inherited from BaseModel | `category.id == 1` |
| `test_category_created_at_inherited` | created_at inherited | `category.created_at` is datetime |
| `test_category_updated_at_inherited` | updated_at inherited | `category.updated_at` is datetime |

#### TestCategoryToDict (4 tests)

| Test | Description | Expected |
|------|-------------|----------|
| `test_to_dict_returns_dictionary` | Returns dict | `isinstance(result, dict) == True` |
| `test_to_dict_contains_all_keys` | Contains all fields | All keys present |
| `test_to_dict_datetime_serialization` | Datetimes as ISO strings | String format verified |
| `test_to_dict_values_correct` | Values match | All values correct |

#### TestCategoryRepr (4 tests)

| Test | Description | Expected |
|------|-------------|----------|
| `test_repr_format` | String format | `"<Category(id=1)>"` |
| `test_repr_with_none_id` | None ID | `"<Category(id=None)>"` |
| `test_repr_class_name` | Class name in repr | Contains "Category" |
| `test_repr_returns_string` | Returns string | `isinstance(result, str) == True` |

#### TestCategoryInvalidData (2 tests)

| Test | Description | Expected |
|------|-------------|----------|
| `test_category_with_empty_name` | Empty string name | Allowed (validation at route level) |
| `test_category_with_none_values` | None values | Allowed |

### Product Model Tests

**File:** `tests/test_product.py`

Similar structure to Category tests, plus:

| Test | Description |
|------|-------------|
| `test_product_price_attribute` | Price is decimal |
| `test_product_stock_quantity_attribute` | Stock is integer |
| `test_product_category_id_attribute` | Foreign key set |

---

## Integration Tests

### Category API Tests

**File:** `tests/test_integration.py`

#### TestCategoryEndpoints

| Test | Method | Endpoint | Expected |
|------|--------|----------|----------|
| `test_get_all_categories_returns_200` | GET | /categories | 200, list response |
| `test_get_all_categories_returns_correct_structure` | GET | /categories | Correct fields |
| `test_get_category_by_id_returns_200` | GET | /categories/{id} | 200, single object |
| `test_get_category_by_invalid_id_returns_404` | GET | /categories/99999 | 404, error response |
| `test_create_category_returns_201` | POST | /categories | 201, created object |
| `test_create_category_without_name_returns_400` | POST | /categories | 400, validation error |
| `test_create_category_with_empty_name_returns_400` | POST | /categories | 400, validation error |
| `test_update_category_returns_200` | PUT | /categories/{id} | 200, updated object |
| `test_update_nonexistent_category_returns_404` | PUT | /categories/99999 | 404, error response |
| `test_delete_category_returns_200` | DELETE | /categories/{id} | 200, success message |
| `test_delete_nonexistent_category_returns_404` | DELETE | /categories/99999 | 404, error response |
| `test_filter_categories_by_name` | GET | /categories?name=... | Filtered results |

### Product API Tests

**File:** `tests/test_integration.py`

#### TestProductEndpoints

| Test | Method | Endpoint | Expected |
|------|--------|----------|----------|
| `test_get_all_products_returns_200` | GET | /products | 200, list response |
| `test_get_product_by_id_returns_200` | GET | /products/{id} | 200, with category_name |
| `test_get_product_by_invalid_id_returns_404` | GET | /products/99999 | 404 |
| `test_create_product_returns_201` | POST | /products | 201 |
| `test_create_product_without_price_returns_400` | POST | /products | 400 |
| `test_create_product_with_negative_price_returns_400` | POST | /products | 400 |
| `test_create_product_with_invalid_category_returns_400` | POST | /products | 400, INVALID_CATEGORY |
| `test_filter_products_by_category` | GET | /products?category_id=1 | Filtered by category |
| `test_filter_products_by_price_range` | GET | /products?min_price=...&max_price=... | Price filtered |
| `test_filter_products_in_stock` | GET | /products?in_stock=true | Only stock > 0 |
| `test_update_product_returns_200` | PUT | /products/{id} | 200 |
| `test_delete_product_returns_200` | DELETE | /products/{id} | 200 |
| `test_update_stock_set` | PATCH | /products/{id}/stock | Stock set |
| `test_update_stock_add` | PATCH | /products/{id}/stock | Stock incremented |
| `test_update_stock_subtract_insufficient` | PATCH | /products/{id}/stock | 400, INSUFFICIENT_STOCK |

### Customer API Tests

**File:** `tests/test_customer_order_integration.py`

#### TestCustomerEndpoints

| Test | Method | Endpoint | Expected |
|------|--------|----------|----------|
| `test_get_all_customers_returns_200` | GET | /customers | 200 |
| `test_create_customer_returns_201` | POST | /customers | 201 |
| `test_create_customer_without_required_fields_returns_400` | POST | /customers | 400 |
| `test_create_customer_with_invalid_email_returns_400` | POST | /customers | 400 |
| `test_create_customer_with_duplicate_email_returns_409` | POST | /customers | 409, DUPLICATE_EMAIL |
| `test_get_customer_by_id_returns_200` | GET | /customers/{id} | 200 |
| `test_get_customer_with_orders_includes_orders` | GET | /customers/{id}?include_orders=true | Orders included |
| `test_get_nonexistent_customer_returns_404` | GET | /customers/99999 | 404 |
| `test_update_customer_returns_200` | PUT | /customers/{id} | 200 |
| `test_delete_customer_returns_200` | DELETE | /customers/{id} | 200 |
| `test_filter_customers_by_name` | GET | /customers?name=... | Filtered |
| `test_filter_customers_by_email` | GET | /customers?email=... | Exact match |

### Order API Tests

**File:** `tests/test_customer_order_integration.py`

#### TestOrderEndpoints

| Test | Method | Endpoint | Expected |
|------|--------|----------|----------|
| `test_get_all_orders_returns_200` | GET | /orders | 200 |
| `test_create_order_returns_201` | POST | /orders | 201, status=pending |
| `test_create_order_decrements_stock` | POST | /orders | Stock reduced |
| `test_create_order_without_items_returns_400` | POST | /orders | 400 |
| `test_create_order_with_insufficient_stock_returns_400` | POST | /orders | 400, INSUFFICIENT_STOCK |
| `test_create_order_with_invalid_customer_returns_404` | POST | /orders | 404 |
| `test_get_order_by_id_returns_200` | GET | /orders/{id} | 200, includes items |
| `test_update_order_status_returns_200` | PATCH | /orders/{id}/status | 200 |
| `test_invalid_status_transition_returns_400` | PATCH | /orders/{id}/status | 400, INVALID_STATUS_TRANSITION |
| `test_cancel_order_restores_stock` | PATCH | /orders/{id}/status | Stock restored |
| `test_filter_orders_by_customer` | GET | /orders?customer_id=... | Filtered |
| `test_filter_orders_by_status` | GET | /orders?status=... | Filtered |
| `test_add_item_to_order_returns_201` | POST | /orders/{id}/items | 201 |
| `test_cannot_modify_non_pending_order` | POST | /orders/{id}/items | 400, ORDER_NOT_MODIFIABLE |
| `test_delete_order_returns_200` | DELETE | /orders/{id} | 200, stock restored |
| `test_get_customer_orders_returns_200` | GET | /customers/{id}/orders | 200 |

#### TestOrderStatusWorkflow

| Test | Description | Expected |
|------|-------------|----------|
| `test_complete_order_workflow` | pending→processing→shipped→delivered | All transitions succeed |
| `test_cannot_delete_delivered_order` | Try to delete delivered order | 400, CANNOT_DELETE_DELIVERED |

### Error Handling Tests

**File:** `tests/test_integration.py`

#### TestErrorHandling

| Test | Description | Expected |
|------|-------------|----------|
| `test_invalid_json_returns_400` | Send invalid JSON | 400 |
| `test_wrong_content_type_is_handled` | Wrong Content-Type | 400 |
| `test_404_for_unknown_endpoint` | Unknown endpoint | 404 |

### Response Format Tests

**File:** `tests/test_integration.py`

#### TestResponseFormat

| Test | Description | Expected |
|------|-------------|----------|
| `test_success_response_format` | Success response structure | `{success: true, data: ...}` |
| `test_error_response_format` | Error response structure | `{success: false, error: {code, message}}` |

---

## Test Execution

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Files

```bash
# Model unit tests
pytest tests/test_category.py -v
pytest tests/test_product.py -v

# Integration tests
pytest tests/test_integration.py -v
pytest tests/test_customer_order_integration.py -v
```

### Run with Coverage

```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Run Specific Test Class

```bash
pytest tests/test_integration.py::TestCategoryEndpoints -v
```

### Run Specific Test

```bash
pytest tests/test_integration.py::TestCategoryEndpoints::test_create_category_returns_201 -v
```

---

## Test Coverage Matrix

### Endpoints Coverage

| Endpoint | Create | Read | Update | Delete | Filter | Special |
|----------|--------|------|--------|--------|--------|---------|
| /categories | ✅ | ✅ | ✅ | ✅ | ✅ | - |
| /products | ✅ | ✅ | ✅ | ✅ | ✅ | Stock ✅ |
| /customers | ✅ | ✅ | ✅ | ✅ | ✅ | Orders ✅ |
| /orders | ✅ | ✅ | Status ✅ | ✅ | ✅ | Items ✅ |

### Business Rules Coverage

| Rule | Tested |
|------|--------|
| Email uniqueness | ✅ |
| Stock decrement on order | ✅ |
| Stock restore on cancel | ✅ |
| Valid status transitions | ✅ |
| Cannot delete customer with orders | ✅ |
| Cannot delete product in orders | ✅ |
| Cannot modify non-pending orders | ✅ |
| Cannot delete delivered orders | ✅ |

### Validation Coverage

| Validation | Tested |
|------------|--------|
| Required fields | ✅ |
| Empty string rejection | ✅ |
| Invalid email format | ✅ |
| Negative price rejection | ✅ |
| Invalid foreign key | ✅ |
| Invalid JSON | ✅ |

### Total Test Count

| Category | Count |
|----------|-------|
| Category Model Unit Tests | 19 |
| Product Model Unit Tests | ~15 |
| Category Integration Tests | 12 |
| Product Integration Tests | 15 |
| Customer Integration Tests | 12 |
| Order Integration Tests | 18 |
| Error Handling Tests | 3 |
| Response Format Tests | 2 |
| **Total** | **~95+** |
