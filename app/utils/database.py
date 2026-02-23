"""
Category Routes Module for Sales By Twilight API.

This module defines all API endpoints for managing product categories.
Implements full CRUD with professional error handling and validation.

Endpoints:
    GET    /categories          - List all categories (with optional filtering)
    GET    /categories/<id>     - Get a single category
    POST   /categories          - Create a new category
    PUT    /categories/<id>     - Update an existing category
    DELETE /categories/<id>     - Delete a category
"""

from flask import Blueprint, request
from app.utils.error_handler import (
    handle_exceptions, success_response, error_response, Errors
)
from app.utils.validators import validate_category_create, validate_category_update
from app.utils.database import get_db_cursor, row_exists, get_row_by_id, QueryBuilder


# Create Blueprint for category routes
category_bp = Blueprint('categories', __name__)


# =============================================================================
# GET /categories - List all categories
# =============================================================================
@category_bp.route('/categories', methods=['GET'])
@handle_exceptions
def get_all_categories():
    """
    Retrieve all categories with optional filtering.
    
    Query Parameters:
        name (str): Filter by category name (partial match)
        sort (str): Sort field (name, created_at). Default: id
        order (str): Sort order (asc, desc). Default: asc
        limit (int): Maximum results to return
        offset (int): Number of results to skip
    
    Returns:
        200: List of categories
        500: Server error
        
    Example:
        GET /categories
        GET /categories?name=produce
        GET /categories?sort=name&order=desc
        GET /categories?limit=10&offset=0
    """
    # Parse query parameters
    name_filter = request.args.get('name')
    sort_field = request.args.get('sort', 'id')
    sort_order = request.args.get('order', 'asc')
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)
    
    # Validate sort field to prevent SQL injection
    allowed_sort_fields = ['id', 'name', 'created_at', 'updated_at']
    if sort_field not in allowed_sort_fields:
        sort_field = 'id'
    
    # Build query
    builder = QueryBuilder('category')
    
    if name_filter:
        builder.where('name', f'%{name_filter}%', 'LIKE')
    
    builder.order_by(sort_field, sort_order)
    
    if limit:
        builder.limit(limit, offset)
    
    query, params = builder.build_select()
    
    with get_db_cursor() as (cursor, conn):
        cursor.execute(query, params)
        categories = cursor.fetchall()
    
    return success_response(categories)


# =============================================================================
# GET /categories/<id> - Get single category
# =============================================================================
@category_bp.route('/categories/<int:category_id>', methods=['GET'])
@handle_exceptions
def get_category(category_id):
    """
    Retrieve a single category by ID.
    
    Path Parameters:
        category_id (int): The category ID
    
    Returns:
        200: Category object
        404: Category not found
        500: Server error
        
    Example:
        GET /categories/1
    """
    category = get_row_by_id('category', category_id)
    
    if category is None:
        return Errors.not_found('Category', category_id)
    
    return success_response(category)


# =============================================================================
# POST /categories - Create new category
# =============================================================================
@category_bp.route('/categories', methods=['POST'])
@handle_exceptions
def create_category():
    """
    Create a new category.
    
    Request Body:
        name (str, required): Category name (max 100 chars)
        description (str, optional): Category description (max 500 chars)
    
    Returns:
        201: Created category
        400: Validation error
        500: Server error
        
    Example:
        POST /categories
        Content-Type: application/json
        {"name": "Bakery", "description": "Fresh bread and pastries"}
    """
    data = request.get_json()
    
    # Validate input
    if data is None:
        return Errors.invalid_json()
    
    is_valid, result = validate_category_create(data)
    if not is_valid:
        return Errors.validation_failed(result)
    
    # Insert into database
    with get_db_cursor(commit=True) as (cursor, conn):
        cursor.execute(
            "INSERT INTO category (name, description) VALUES (%s, %s)",
            (result['name'], result.get('description'))
        )
        new_id = cursor.lastrowid
        
        # Fetch the created category
        cursor.execute("SELECT * FROM category WHERE id = %s", (new_id,))
        new_category = cursor.fetchone()
    
    return success_response(new_category, 201, "Category created successfully")


# =============================================================================
# PUT /categories/<id> - Update category
# =============================================================================
@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
@handle_exceptions
def update_category(category_id):
    """
    Update an existing category.
    
    Path Parameters:
        category_id (int): The category ID
    
    Request Body:
        name (str, optional): New category name
        description (str, optional): New category description
    
    Returns:
        200: Updated category
        400: Validation error
        404: Category not found
        500: Server error
        
    Example:
        PUT /categories/1
        Content-Type: application/json
        {"name": "Fresh Produce & Vegetables"}
    """
    # Check if category exists
    if not row_exists('category', 'id', category_id):
        return Errors.not_found('Category', category_id)
    
    data = request.get_json()
    
    # Validate input
    if data is None:
        return Errors.invalid_json()
    
    is_valid, result = validate_category_update(data)
    if not is_valid:
        return Errors.validation_failed(result)
    
    # Build and execute update query
    builder = QueryBuilder('category')
    builder.set('name', result.get('name'))
    builder.set('description', result.get('description'))
    builder.where('id', category_id)
    
    query, params = builder.build_update()
    
    with get_db_cursor(commit=True) as (cursor, conn):
        cursor.execute(query, params)
        
        # Fetch the updated category
        cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
        updated_category = cursor.fetchone()
    
    return success_response(updated_category, message="Category updated successfully")


# =============================================================================
# DELETE /categories/<id> - Delete category
# =============================================================================
@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@handle_exceptions
def delete_category(category_id):
    """
    Delete a category.
    
    Path Parameters:
        category_id (int): The category ID
    
    Returns:
        200: Success message
        404: Category not found
        500: Server error
        
    Note:
        Products in this category will have their category_id set to NULL.
        
    Example:
        DELETE /categories/4
    """
    # Check if category exists
    if not row_exists('category', 'id', category_id):
        return Errors.not_found('Category', category_id)
    
    with get_db_cursor(commit=True) as (cursor, conn):
        cursor.execute("DELETE FROM category WHERE id = %s", (category_id,))
    
    return success_response(None, message="Category deleted successfully")