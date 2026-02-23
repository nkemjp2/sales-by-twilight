"""
Integration Tests for Sales By Twilight API.

These tests verify the API endpoints work correctly end-to-end,
including database operations and HTTP responses.

Run with: pytest tests/test_integration.py -v
"""

import pytest
import json
from app import create_app
from app.utils.database import get_db_cursor


@pytest.fixture(scope='module')
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture(scope='module')
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def cleanup_test_data():
    """
    Clean up test data after each test.
    Yields control to the test, then cleans up.
    """
    yield
    # Cleanup: Remove test categories and products created during tests
    with get_db_cursor(commit=True) as (cursor, conn):
        cursor.execute("DELETE FROM product WHERE name LIKE 'Test%'")
        cursor.execute("DELETE FROM category WHERE name LIKE 'Test%'")


# =============================================================================
# CATEGORY ENDPOINT TESTS
# =============================================================================

class TestCategoryEndpoints:
    """Integration tests for category endpoints."""
    
    def test_get_all_categories_returns_200(self, client):
        """GET /categories should return 200 and a list."""
        response = client.get('/categories')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
    
    def test_get_all_categories_returns_correct_structure(self, client):
        """GET /categories should return categories with correct fields."""
        response = client.get('/categories')
        data = json.loads(response.data)
        
        if data['data']:  # If there are categories
            category = data['data'][0]
            assert 'id' in category
            assert 'name' in category
            assert 'description' in category
            assert 'created_at' in category
            assert 'updated_at' in category
    
    def test_get_category_by_id_returns_200(self, client):
        """GET /categories/<id> should return 200 for existing category."""
        # First, get a category that exists
        response = client.get('/categories')
        data = json.loads(response.data)
        
        if data['data']:
            category_id = data['data'][0]['id']
            response = client.get(f'/categories/{category_id}')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['data']['id'] == category_id
    
    def test_get_category_by_invalid_id_returns_404(self, client):
        """GET /categories/<id> should return 404 for non-existent category."""
        response = client.get('/categories/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error']['code'] == 'RESOURCE_NOT_FOUND'
    
    def test_create_category_returns_201(self, client, cleanup_test_data):
        """POST /categories should create a category and return 201."""
        payload = {
            'name': 'Test Category',
            'description': 'A test category for integration testing'
        }
        
        response = client.post(
            '/categories',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'Test Category'
        assert 'id' in data['data']
    
    def test_create_category_without_name_returns_400(self, client):
        """POST /categories without name should return 400."""
        payload = {
            'description': 'Missing name field'
        }
        
        response = client.post(
            '/categories',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_create_category_with_empty_name_returns_400(self, client):
        """POST /categories with empty name should return 400."""
        payload = {
            'name': '   ',
            'description': 'Empty name'
        }
        
        response = client.post(
            '/categories',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_update_category_returns_200(self, client, cleanup_test_data):
        """PUT /categories/<id> should update and return 200."""
        # First create a category
        create_response = client.post(
            '/categories',
            data=json.dumps({'name': 'Test Update Category'}),
            content_type='application/json'
        )
        created = json.loads(create_response.data)
        category_id = created['data']['id']
        
        # Now update it
        update_payload = {'name': 'Test Updated Name'}
        response = client.put(
            f'/categories/{category_id}',
            data=json.dumps(update_payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['name'] == 'Test Updated Name'
    
    def test_update_nonexistent_category_returns_404(self, client):
        """PUT /categories/<id> for non-existent category should return 404."""
        response = client.put(
            '/categories/99999',
            data=json.dumps({'name': 'New Name'}),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_category_returns_200(self, client, cleanup_test_data):
        """DELETE /categories/<id> should delete and return 200."""
        # First create a category
        create_response = client.post(
            '/categories',
            data=json.dumps({'name': 'Test Delete Category'}),
            content_type='application/json'
        )
        created = json.loads(create_response.data)
        category_id = created['data']['id']
        
        # Now delete it
        response = client.delete(f'/categories/{category_id}')
        
        assert response.status_code == 200
        
        # Verify it's gone
        get_response = client.get(f'/categories/{category_id}')
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_category_returns_404(self, client):
        """DELETE /categories/<id> for non-existent category should return 404."""
        response = client.delete('/categories/99999')
        
        assert response.status_code == 404
    
    def test_filter_categories_by_name(self, client, cleanup_test_data):
        """GET /categories?name=... should filter by name."""
        # Create test categories
        client.post(
            '/categories',
            data=json.dumps({'name': 'Test Fresh Produce'}),
            content_type='application/json'
        )
        client.post(
            '/categories',
            data=json.dumps({'name': 'Test Dairy'}),
            content_type='application/json'
        )
        
        # Filter by name
        response = client.get('/categories?name=Fresh')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        # All returned categories should contain 'Fresh' in name
        for cat in data['data']:
            assert 'Fresh' in cat['name'] or 'fresh' in cat['name'].lower()


# =============================================================================
# PRODUCT ENDPOINT TESTS
# =============================================================================

class TestProductEndpoints:
    """Integration tests for product endpoints."""
    
    def test_get_all_products_returns_200(self, client):
        """GET /products should return 200 and a list."""
        response = client.get('/products')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
    
    def test_get_product_by_id_returns_200(self, client):
        """GET /products/<id> should return 200 for existing product."""
        response = client.get('/products')
        data = json.loads(response.data)
        
        if data['data']:
            product_id = data['data'][0]['id']
            response = client.get(f'/products/{product_id}')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
    
    def test_get_product_by_invalid_id_returns_404(self, client):
        """GET /products/<id> should return 404 for non-existent product."""
        response = client.get('/products/99999')
        
        assert response.status_code == 404
    
    def test_create_product_returns_201(self, client, cleanup_test_data):
        """POST /products should create a product and return 201."""
        payload = {
            'name': 'Test Product',
            'description': 'A test product',
            'price': 9.99,
            'stock_quantity': 50
        }
        
        response = client.post(
            '/products',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'Test Product'
        assert data['data']['price'] == 9.99
    
    def test_create_product_without_price_returns_400(self, client):
        """POST /products without price should return 400."""
        payload = {
            'name': 'Test Product No Price'
        }
        
        response = client.post(
            '/products',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_create_product_with_negative_price_returns_400(self, client):
        """POST /products with negative price should return 400."""
        payload = {
            'name': 'Test Product Negative',
            'price': -5.00
        }
        
        response = client.post(
            '/products',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_create_product_with_invalid_category_returns_400(self, client):
        """POST /products with non-existent category_id should return 400."""
        payload = {
            'name': 'Test Product Bad Category',
            'price': 9.99,
            'category_id': 99999
        }
        
        response = client.post(
            '/products',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'INVALID_CATEGORY' in data['error']['code']
    
    def test_filter_products_by_category(self, client):
        """GET /products?category_id=... should filter by category."""
        # Get products filtered by category 1
        response = client.get('/products?category_id=1')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        # All returned products should have category_id = 1
        for product in data['data']:
            assert product['category_id'] == 1
    
    def test_filter_products_by_price_range(self, client):
        """GET /products?min_price=...&max_price=... should filter by price."""
        min_price = 1.00
        max_price = 5.00
        
        response = client.get(f'/products?min_price={min_price}&max_price={max_price}')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        for product in data['data']:
            assert min_price <= product['price'] <= max_price
    
    def test_filter_products_in_stock(self, client):
        """GET /products?in_stock=true should return only products with stock."""
        response = client.get('/products?in_stock=true')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        for product in data['data']:
            assert product['stock_quantity'] > 0
    
    def test_update_product_returns_200(self, client, cleanup_test_data):
        """PUT /products/<id> should update and return 200."""
        # First create a product
        create_response = client.post(
            '/products',
            data=json.dumps({'name': 'Test Update Product', 'price': 5.00}),
            content_type='application/json'
        )
        created = json.loads(create_response.data)
        product_id = created['data']['id']
        
        # Now update it
        update_payload = {'price': 7.50}
        response = client.put(
            f'/products/{product_id}',
            data=json.dumps(update_payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['price'] == 7.50
    
    def test_delete_product_returns_200(self, client, cleanup_test_data):
        """DELETE /products/<id> should delete and return 200."""
        # First create a product
        create_response = client.post(
            '/products',
            data=json.dumps({'name': 'Test Delete Product', 'price': 5.00}),
            content_type='application/json'
        )
        created = json.loads(create_response.data)
        product_id = created['data']['id']
        
        # Now delete it
        response = client.delete(f'/products/{product_id}')
        
        assert response.status_code == 200
        
        # Verify it's gone
        get_response = client.get(f'/products/{product_id}')
        assert get_response.status_code == 404
    
    def test_update_stock_set(self, client, cleanup_test_data):
        """PATCH /products/<id>/stock should set stock quantity."""
        # First create a product
        create_response = client.post(
            '/products',
            data=json.dumps({'name': 'Test Stock Product', 'price': 5.00, 'stock_quantity': 10}),
            content_type='application/json'
        )
        created = json.loads(create_response.data)
        product_id = created['data']['id']
        
        # Update stock
        response = client.patch(
            f'/products/{product_id}/stock',
            data=json.dumps({'quantity': 50}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['stock_quantity'] == 50
    
    def test_update_stock_add(self, client, cleanup_test_data):
        """PATCH /products/<id>/stock with operation=add should add to stock."""
        # First create a product
        create_response = client.post(
            '/products',
            data=json.dumps({'name': 'Test Stock Add', 'price': 5.00, 'stock_quantity': 10}),
            content_type='application/json'
        )
        created = json.loads(create_response.data)
        product_id = created['data']['id']
        
        # Add to stock
        response = client.patch(
            f'/products/{product_id}/stock',
            data=json.dumps({'quantity': 25, 'operation': 'add'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['stock_quantity'] == 35  # 10 + 25
    
    def test_update_stock_subtract_insufficient(self, client, cleanup_test_data):
        """PATCH /products/<id>/stock subtract more than available should fail."""
        # First create a product
        create_response = client.post(
            '/products',
            data=json.dumps({'name': 'Test Stock Subtract', 'price': 5.00, 'stock_quantity': 10}),
            content_type='application/json'
        )
        created = json.loads(create_response.data)
        product_id = created['data']['id']
        
        # Try to subtract more than available
        response = client.patch(
            f'/products/{product_id}/stock',
            data=json.dumps({'quantity': 20, 'operation': 'subtract'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'INSUFFICIENT_STOCK' in data['error']['code']


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

class TestErrorHandling:
    """Test error handling across the API."""
    
    def test_invalid_json_returns_400(self, client):
        """Posting invalid JSON should return 400."""
        response = client.post(
            '/categories',
            data='not valid json',
            content_type='application/json'
        )
        
        # Flask may return 400 or our custom error
        assert response.status_code in (400, 415)
    
    def test_wrong_content_type_is_handled(self, client):
        """Posting with wrong content type should be handled."""
        response = client.post(
            '/categories',
            data='name=Test',
            content_type='application/x-www-form-urlencoded'
        )
        
        assert response.status_code == 400
    
    def test_404_for_unknown_endpoint(self, client):
        """Accessing unknown endpoint should return 404."""
        response = client.get('/unknown-endpoint')
        
        assert response.status_code == 404


# =============================================================================
# RESPONSE FORMAT TESTS
# =============================================================================

class TestResponseFormat:
    """Test that responses follow consistent format."""
    
    def test_success_response_format(self, client):
        """Success responses should have correct format."""
        response = client.get('/categories')
        data = json.loads(response.data)
        
        assert 'success' in data
        assert 'data' in data
        assert data['success'] is True
    
    def test_error_response_format(self, client):
        """Error responses should have correct format."""
        response = client.get('/categories/99999')
        data = json.loads(response.data)
        
        assert 'success' in data
        assert 'error' in data
        assert data['success'] is False
        assert 'code' in data['error']
        assert 'message' in data['error']