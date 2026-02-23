"""
Product Routes Module for Sales By Twilight API.

This module defines all API endpoints for managing products.
Implements full CRUD with filtering, validation, and error handling.

Endpoints:
    GET    /products          - List all products (with filtering)
    GET    /products/<id>     - Get a single product
    POST   /products          - Create a new product
    PUT    /products/<id>     - Update an existing product
    DELETE /products/<id>     - Delete a product
"""

from flask import Blueprint, request
from app.utils.error_handler import (
    handle_exceptions, success_response, error_response, Errors
)
from app.utils.validators import validate_product_create, validate_product_update
from app.utils.database import get_db_cursor, row_exists, get_row_by_id, QueryBuilder


# Create Blueprint for product routes
product_bp = Blueprint('products', __name__)


# =============================================================================
# GET /products - List all products with filtering
# =============================================================================
@product_bp.route('/products', methods=['GET'])
@handle_exceptions
def get_all_products():
    """
    Retrieve all products with optional filtering.
    
    Query Parameters:
        category_id (int): Filter by category ID
        name (str): Filter by product name (partial match)
        min_price (float): Minimum price filter
        max_price (float): Maximum price filter
        in_stock (bool): If true, only return products with stock > 0
        sort (str): Sort field (name, price, created_at). Default: id
        order (str): Sort order (asc, desc). Default: asc
        limit (int): Maximum results to return
        offset (int): Number of results to skip
    
    Returns:
        200: List of products
        500: Server error
        
    Example:
        GET /products
        GET /products?category_id=1
        GET /products?min_price=5&max_price=20
        GET /products?in_stock=true&sort=price&order=asc
        GET /products?name=organic&limit=10
    """
    # Parse query parameters
    category_id = request.args.get('category_id', type=int)
    name_filter = request.args.get('name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock = request.args.get('in_stock')
    sort_field = request.args.get('sort', 'id')
    sort_order = request.args.get('order', 'asc')
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)
    
    # Validate sort field
    allowed_sort_fields = ['id', 'name', 'price', 'stock_quantity', 'created_at', 'updated_at']
    if sort_field not in allowed_sort_fields:
        sort_field = 'id'
    
    # Build query dynamically
    builder = QueryBuilder('product')
    
    if category_id is not None:
        builder.where('category_id', category_id)
    
    if name_filter:
        builder.where('name', f'%{name_filter}%', 'LIKE')
    
    if min_price is not None:
        builder.where('price', min_price, '>=')
    
    if max_price is not None:
        builder.where('price', max_price, '<=')
    
    if in_stock and in_stock.lower() == 'true':
        builder.where('stock_quantity', 0, '>')
    
    builder.order_by(sort_field, sort_order)
    
    if limit:
        builder.limit(limit, offset)
    
    query, params = builder.build_select()
    
    with get_db_cursor() as (cursor, conn):
        cursor.execute(query, params)
        products = cursor.fetchall()
    
    return success_response(products)


# =============================================================================
# GET /products/<id> - Get single product
# =============================================================================
@product_bp.route('/products/<int:product_id>', methods=['GET'])
@handle_exceptions
def get_product(product_id):
    """
    Retrieve a single product by ID.
    
    Path Parameters:
        product_id (int): The product ID
    
    Returns:
        200: Product object (includes category info)
        404: Product not found
        500: Server error
        
    Example:
        GET /products/1
    """
    with get_db_cursor() as (cursor, conn):
        # Join with category to include category name
        cursor.execute("""
            SELECT 
                p.*,
                c.name as category_name
            FROM product p
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.id = %s
        """, (product_id,))
        product = cursor.fetchone()
    
    if product is None:
        return Errors.not_found('Product', product_id)
    
    return success_response(product)


# =============================================================================
# POST /products - Create new product
# =============================================================================
@product_bp.route('/products', methods=['POST'])
@handle_exceptions
def create_product():
    """
    Create a new product.
    
    Request Body:
        name (str, required): Product name (max 200 chars)
        description (str, optional): Product description
        price (float, required): Product price (must be > 0)
        stock_quantity (int, optional): Initial stock (default 0, must be >= 0)
        category_id (int, optional): Category ID
    
    Returns:
        201: Created product
        400: Validation error or invalid category_id
        500: Server error
        
    Example:
        POST /products
        Content-Type: application/json
        {
            "name": "Organic Apples",
            "description": "Fresh organic apples from local farms",
            "price": 3.99,
            "stock_quantity": 100,
            "category_id": 1
        }
    """
    data = request.get_json()
    
    if data is None:
        return Errors.invalid_json()
    
    # Validate input
    is_valid, result = validate_product_create(data)
    if not is_valid:
        return Errors.validation_failed(result)
    
    # Verify category exists if provided
    if result.get('category_id'):
        if not row_exists('category', 'id', result['category_id']):
            return error_response(
                f"Category with ID {result['category_id']} does not exist",
                400,
                "INVALID_CATEGORY"
            )
    
    # Insert into database
    with get_db_cursor(commit=True) as (cursor, conn):
        cursor.execute("""
            INSERT INTO product (name, description, price, stock_quantity, category_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            result['name'],
            result.get('description'),
            result['price'],
            result.get('stock_quantity', 0),
            result.get('category_id')
        ))
        new_id = cursor.lastrowid
        
        # Fetch the created product with category info
        cursor.execute("""
            SELECT p.*, c.name as category_name
            FROM product p
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.id = %s
        """, (new_id,))
        new_product = cursor.fetchone()
    
    return success_response(new_product, 201, "Product created successfully")


# =============================================================================
# PUT /products/<id> - Update product
# =============================================================================
@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@handle_exceptions
def update_product(product_id):
    """
    Update an existing product.
    
    Path Parameters:
        product_id (int): The product ID
    
    Request Body:
        name (str, optional): New product name
        description (str, optional): New description
        price (float, optional): New price
        stock_quantity (int, optional): New stock quantity
        category_id (int, optional): New category ID
    
    Returns:
        200: Updated product
        400: Validation error
        404: Product not found
        500: Server error
        
    Example:
        PUT /products/1
        Content-Type: application/json
        {"price": 4.49, "stock_quantity": 75}
    """
    # Check if product exists
    if not row_exists('product', 'id', product_id):
        return Errors.not_found('Product', product_id)
    
    data = request.get_json()
    
    if data is None:
        return Errors.invalid_json()
    
    # Validate input
    is_valid, result = validate_product_update(data)
    if not is_valid:
        return Errors.validation_failed(result)
    
    # Verify category exists if being updated
    if result.get('category_id'):
        if not row_exists('category', 'id', result['category_id']):
            return error_response(
                f"Category with ID {result['category_id']} does not exist",
                400,
                "INVALID_CATEGORY"
            )
    
    # Build and execute update query
    builder = QueryBuilder('product')
    builder.set('name', result.get('name'))
    builder.set('description', result.get('description'))
    builder.set('price', result.get('price'))
    builder.set('stock_quantity', result.get('stock_quantity'))
    builder.set('category_id', result.get('category_id'))
    builder.where('id', product_id)
    
    query, params = builder.build_update()
    
    with get_db_cursor(commit=True) as (cursor, conn):
        cursor.execute(query, params)
        
        # Fetch the updated product
        cursor.execute("""
            SELECT p.*, c.name as category_name
            FROM product p
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.id = %s
        """, (product_id,))
        updated_product = cursor.fetchone()
    
    return success_response(updated_product, message="Product updated successfully")


# =============================================================================
# DELETE /products/<id> - Delete product
# =============================================================================
@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@handle_exceptions
def delete_product(product_id):
    """
    Delete a product.
    
    Path Parameters:
        product_id (int): The product ID
    
    Returns:
        200: Success message
        404: Product not found
        409: Product is referenced in orders (cannot delete)
        500: Server error
        
    Note:
        Products that are part of existing orders cannot be deleted.
        
    Example:
        DELETE /products/5
    """
    # Check if product exists
    if not row_exists('product', 'id', product_id):
        return Errors.not_found('Product', product_id)
    
    # Check if product is in any orders
    if row_exists('order_item', 'product_id', product_id):
        return error_response(
            "Cannot delete product that is part of existing orders",
            409,
            "PRODUCT_IN_USE"
        )
    
    with get_db_cursor(commit=True) as (cursor, conn):
        cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    
    return success_response(None, message="Product deleted successfully")


# =============================================================================
# PATCH /products/<id>/stock - Update stock quantity
# =============================================================================
@product_bp.route('/products/<int:product_id>/stock', methods=['PATCH'])
@handle_exceptions
def update_stock(product_id):
    """
    Update product stock quantity (increment or set absolute value).
    
    Path Parameters:
        product_id (int): The product ID
    
    Request Body:
        quantity (int, required): New stock quantity OR amount to add/subtract
        operation (str, optional): 'set', 'add', or 'subtract'. Default: 'set'
    
    Returns:
        200: Updated product with new stock
        400: Validation error or insufficient stock
        404: Product not found
        500: Server error
        
    Example (set absolute):
        PATCH /products/1/stock
        {"quantity": 100}
        
    Example (add):
        PATCH /products/1/stock
        {"quantity": 50, "operation": "add"}
        
    Example (subtract):
        PATCH /products/1/stock
        {"quantity": 10, "operation": "subtract"}
    """
    # Check if product exists
    product = get_row_by_id('product', product_id)
    if product is None:
        return Errors.not_found('Product', product_id)
    
    data = request.get_json()
    
    if data is None:
        return Errors.invalid_json()
    
    # Validate quantity
    if 'quantity' not in data:
        return Errors.missing_field('quantity')
    
    try:
        quantity = int(data['quantity'])
    except (TypeError, ValueError):
        return Errors.invalid_type('quantity', 'integer')
    
    operation = data.get('operation', 'set').lower()
    if operation not in ('set', 'add', 'subtract'):
        return error_response(
            "Operation must be 'set', 'add', or 'subtract'",
            400,
            "INVALID_OPERATION"
        )
    
    # Calculate new stock
    current_stock = product['stock_quantity']
    
    if operation == 'set':
        if quantity < 0:
            return error_response("Stock quantity cannot be negative", 400, "INVALID_QUANTITY")
        new_stock = quantity
    elif operation == 'add':
        new_stock = current_stock + quantity
    else:  # subtract
        new_stock = current_stock - quantity
        if new_stock < 0:
            return error_response(
                f"Insufficient stock. Current: {current_stock}, Requested: {quantity}",
                400,
                "INSUFFICIENT_STOCK"
            )
    
    # Update stock
    with get_db_cursor(commit=True) as (cursor, conn):
        cursor.execute(
            "UPDATE product SET stock_quantity = %s WHERE id = %s",
            (new_stock, product_id)
        )
        
        # Fetch updated product
        cursor.execute("SELECT * FROM product WHERE id = %s", (product_id,))
        updated_product = cursor.fetchone()
    
    return success_response(
        updated_product,
        message=f"Stock updated from {current_stock} to {new_stock}"
    )