"""
Category Routes Module for Sales By Twilight API.

This module defines all API endpoints for managing product categories.
It implements full CRUD (Create, Read, Update, Delete) operations.

Endpoints:
    GET    /categories          - Retrieve all categories
    GET    /categories/<id>     - Retrieve a single category
    POST   /categories          - Create a new category
    PUT    /categories/<id>     - Update an existing category
    DELETE /categories/<id>     - Delete a category
"""

from flask import Blueprint, jsonify, request
import mysql.connector
import os

# ==================== BLUEPRINT CREATION ====================
# A Blueprint is a way to organize related routes into groups.
# 'categories' is the name of this blueprint (used for URL generation)
# __name__ helps Flask locate the blueprint's resources
category_bp = Blueprint('categories', __name__)


# ==================== DATABASE CONNECTION ====================
def get_db_connection():
    """
    Create and return a connection to the MySQL database.
    
    This function reads database configuration from environment variables,
    which are loaded from the .env file. Using environment variables keeps
    sensitive data (like passwords) out of the code.
    
    Returns:
        mysql.connector.connection.MySQLConnection: A database connection object
        
    Raises:
        mysql.connector.Error: If connection fails
    """
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),      # Database server address
        port=int(os.getenv('DB_PORT', 3306)),        # MySQL default port
        database=os.getenv('DB_NAME', 'sales_by_twilight'),  # Database name
        user=os.getenv('DB_USER', 'root'),           # Database username
        password=os.getenv('DB_PASSWORD', '')        # Database password
    )
    return connection


# ==================== READ: GET ALL CATEGORIES ====================
@category_bp.route('/categories', methods=['GET'])
def get_all_categories():
    """
    Retrieve all categories from the database.
    
    HTTP Method: GET
    URL: /categories
    
    Returns:
        JSON array of all categories with 200 status code
        JSON error message with 500 status code if database error occurs
        
    Example Response (200):
        [
            {
                "id": 1,
                "name": "Fresh Produce",
                "description": "Fruits and vegetables",
                "created_at": "2026-02-23T06:42:01",
                "updated_at": "2026-02-23T06:42:01"
            }
        ]
    """
    try:
        # Establish database connection
        connection = get_db_connection()
        
        # Create a cursor with dictionary=True to get results as dictionaries
        # instead of tuples. This makes it easier to convert to JSON.
        cursor = connection.cursor(dictionary=True)
        
        # Execute SQL query to get all categories
        cursor.execute("SELECT * FROM category ORDER BY id")
        
        # Fetch all rows from the result
        categories = cursor.fetchall()
        
        # Clean up: always close cursor and connection
        cursor.close()
        connection.close()
        
        # Return JSON response with 200 OK status
        return jsonify(categories), 200
        
    except mysql.connector.Error as err:
        # Handle database-specific errors
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# ==================== READ: GET SINGLE CATEGORY ====================
@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Retrieve a single category by its ID.
    
    HTTP Method: GET
    URL: /categories/<id>
    
    Args:
        category_id (int): The unique identifier of the category
        
    Returns:
        JSON object of the category with 200 status code
        JSON error message with 404 if category not found
        JSON error message with 500 if database error occurs
        
    Example Response (200):
        {
            "id": 1,
            "name": "Fresh Produce",
            "description": "Fruits and vegetables",
            "created_at": "2026-02-23T06:42:01",
            "updated_at": "2026-02-23T06:42:01"
        }
        
    Example Response (404):
        {"error": "Category not found"}
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Use parameterized query to prevent SQL injection
        # The %s is a placeholder that gets safely replaced with category_id
        cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
        
        # fetchone() returns a single row or None if not found
        category = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        # Check if category was found
        if category is None:
            return jsonify({"error": "Category not found"}), 404
            
        return jsonify(category), 200
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# ==================== CREATE: POST NEW CATEGORY ====================
@category_bp.route('/categories', methods=['POST'])
def create_category():
    """
    Create a new category.
    
    HTTP Method: POST
    URL: /categories
    Content-Type: application/json
    
    Request Body:
        {
            "name": "Category Name",        (required)
            "description": "Description"    (optional)
        }
        
    Returns:
        JSON object of created category with 201 status code
        JSON error message with 400 if validation fails
        JSON error message with 500 if database error occurs
        
    Example Request:
        POST /categories
        Content-Type: application/json
        {
            "name": "Bakery",
            "description": "Fresh bread and pastries"
        }
        
    Example Response (201):
        {
            "id": 4,
            "name": "Bakery",
            "description": "Fresh bread and pastries",
            "created_at": "2026-02-23T10:30:00",
            "updated_at": "2026-02-23T10:30:00"
        }
        
    Example Response (400):
        {"error": "Missing required field: name"}
    """
    try:
        # Get JSON data from request body
        # request.get_json() parses the JSON payload sent by the client
        data = request.get_json()
        
        # ===== INPUT VALIDATION =====
        # Check if request body is empty or not JSON
        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        # Check if required field 'name' is present
        if 'name' not in data or data['name'] is None:
            return jsonify({"error": "Missing required field: name"}), 400
        
        # Check if name is not empty string
        if not data['name'].strip():
            return jsonify({"error": "Category name cannot be empty"}), 400
        
        # Extract values from request data
        name = data['name'].strip()  # .strip() removes leading/trailing whitespace
        description = data.get('description', None)  # .get() returns None if key doesn't exist
        
        # If description provided, strip whitespace
        if description:
            description = description.strip()
        
        # ===== DATABASE INSERT =====
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Insert new category into database
        # Using parameterized query to prevent SQL injection
        insert_query = """
            INSERT INTO category (name, description)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (name, description))
        
        # Commit the transaction to save changes
        # Without commit(), the insert would be rolled back
        connection.commit()
        
        # Get the ID of the newly inserted row
        new_id = cursor.lastrowid
        
        # Fetch the complete newly created category
        cursor.execute("SELECT * FROM category WHERE id = %s", (new_id,))
        new_category = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        # Return the created category with 201 Created status
        # 201 indicates a new resource was successfully created
        return jsonify(new_category), 201
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# ==================== UPDATE: PUT EXISTING CATEGORY ====================
@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Update an existing category.
    
    HTTP Method: PUT
    URL: /categories/<id>
    Content-Type: application/json
    
    Args:
        category_id (int): The unique identifier of the category to update
        
    Request Body:
        {
            "name": "New Name",             (optional)
            "description": "New Description" (optional)
        }
        
    Returns:
        JSON object of updated category with 200 status code
        JSON error message with 400 if validation fails
        JSON error message with 404 if category not found
        JSON error message with 500 if database error occurs
        
    Example Request:
        PUT /categories/1
        Content-Type: application/json
        {
            "name": "Fresh Produce & Vegetables",
            "description": "All fresh fruits and vegetables"
        }
        
    Example Response (200):
        {
            "id": 1,
            "name": "Fresh Produce & Vegetables",
            "description": "All fresh fruits and vegetables",
            "created_at": "2026-02-23T06:42:01",
            "updated_at": "2026-02-23T11:00:00"
        }
    """
    try:
        # Get JSON data from request body
        data = request.get_json()
        
        # ===== INPUT VALIDATION =====
        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        # Check if at least one field is provided to update
        if 'name' not in data and 'description' not in data:
            return jsonify({"error": "At least one field (name or description) must be provided"}), 400
        
        # Validate name if provided
        if 'name' in data:
            if data['name'] is None or not data['name'].strip():
                return jsonify({"error": "Category name cannot be empty"}), 400
        
        # ===== CHECK IF CATEGORY EXISTS =====
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
        existing_category = cursor.fetchone()
        
        if existing_category is None:
            cursor.close()
            connection.close()
            return jsonify({"error": "Category not found"}), 404
        
        # ===== BUILD UPDATE QUERY DYNAMICALLY =====
        # Only update fields that were provided in the request
        update_fields = []
        update_values = []
        
        if 'name' in data:
            update_fields.append("name = %s")
            update_values.append(data['name'].strip())
            
        if 'description' in data:
            update_fields.append("description = %s")
            # Allow description to be set to None (null)
            description = data['description']
            if description:
                description = description.strip()
            update_values.append(description)
        
        # Add category_id to the end for the WHERE clause
        update_values.append(category_id)
        
        # Construct the UPDATE query
        # Example: "UPDATE category SET name = %s, description = %s WHERE id = %s"
        update_query = f"""
            UPDATE category 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        
        cursor.execute(update_query, tuple(update_values))
        connection.commit()
        
        # Fetch the updated category
        cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
        updated_category = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        # Return the updated category with 200 OK status
        return jsonify(updated_category), 200
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# ==================== DELETE: REMOVE CATEGORY ====================
@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """
    Delete a category by its ID.
    
    HTTP Method: DELETE
    URL: /categories/<id>
    
    Args:
        category_id (int): The unique identifier of the category to delete
        
    Returns:
        JSON success message with 200 status code
        JSON error message with 404 if category not found
        JSON error message with 500 if database error occurs
        
    Note:
        Products in this category will have their category_id set to NULL
        (ON DELETE SET NULL in database schema)
        
    Example Response (200):
        {"message": "Category deleted successfully"}
        
    Example Response (404):
        {"error": "Category not found"}
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # ===== CHECK IF CATEGORY EXISTS =====
        cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
        category = cursor.fetchone()
        
        if category is None:
            cursor.close()
            connection.close()
            return jsonify({"error": "Category not found"}), 404
        
        # ===== DELETE THE CATEGORY =====
        cursor.execute("DELETE FROM category WHERE id = %s", (category_id,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        # Return success message with 200 OK
        # Alternative: return '', 204 (No Content - empty response)
        return jsonify({"message": "Category deleted successfully"}), 200
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500