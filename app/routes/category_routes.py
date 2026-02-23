"""
Category routes for Sales By Twilight API.
Handles all category-related endpoints.
"""

from flask import Blueprint, jsonify
import mysql.connector
import os

# Create a Blueprint for category routes
category_bp = Blueprint('categories', __name__)


def get_db_connection():
    """
    Create and return a database connection.
    
    Returns:
        mysql.connector.connection: Database connection object
    """
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        database=os.getenv('DB_NAME', 'sales_by_twilight'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )
    return connection


@category_bp.route('/categories', methods=['GET'])
def get_all_categories():
    """
    Get all categories from the database.
    
    Returns:
        JSON response with list of all categories
        HTTP 200 on success
        HTTP 500 on database error
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(categories), 200
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Get a single category by ID.
    
    Args:
        category_id: The ID of the category to retrieve
        
    Returns:
        JSON response with category data
        HTTP 200 on success
        HTTP 404 if category not found
        HTTP 500 on database error
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
        category = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if category is None:
            return jsonify({"error": "Category not found"}), 404
            
        return jsonify(category), 200
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500