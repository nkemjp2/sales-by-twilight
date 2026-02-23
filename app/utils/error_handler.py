"""
Error Handling Module for Sales By Twilight API.

This module provides consistent error responses across all API endpoints.
Following RFC 7807 (Problem Details for HTTP APIs) principles.
"""

from flask import jsonify
from functools import wraps
import mysql.connector


class APIError(Exception):
    """
    Custom exception for API errors.
    
    Allows raising errors with specific status codes and messages
    that will be consistently formatted in the response.
    """
    
    def __init__(self, message, status_code=400, error_code=None, details=None):
        """
        Initialize an API error.
        
        Args:
            message: Human-readable error message
            status_code: HTTP status code (default 400)
            error_code: Machine-readable error code (e.g., 'VALIDATION_ERROR')
            details: Additional error details (dict or list)
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self._default_error_code(status_code)
        self.details = details
    
    def _default_error_code(self, status_code):
        """Map status codes to default error codes."""
        mapping = {
            400: 'BAD_REQUEST',
            401: 'UNAUTHORIZED',
            403: 'FORBIDDEN',
            404: 'NOT_FOUND',
            409: 'CONFLICT',
            422: 'UNPROCESSABLE_ENTITY',
            500: 'INTERNAL_ERROR'
        }
        return mapping.get(status_code, 'ERROR')
    
    def to_dict(self):
        """Convert error to dictionary for JSON response."""
        response = {
            'success': False,
            'error': {
                'code': self.error_code,
                'message': self.message
            }
        }
        if self.details:
            response['error']['details'] = self.details
        return response


def error_response(message, status_code=400, error_code=None, details=None):
    """
    Create a consistent error response.
    
    Args:
        message: Human-readable error message
        status_code: HTTP status code
        error_code: Machine-readable error code
        details: Additional error details
        
    Returns:
        tuple: (JSON response, status code)
        
    Example:
        return error_response("Category not found", 404, "RESOURCE_NOT_FOUND")
    """
    error = APIError(message, status_code, error_code, details)
    return jsonify(error.to_dict()), status_code


def success_response(data, status_code=200, message=None):
    """
    Create a consistent success response.
    
    Args:
        data: The response data (dict, list, or None)
        status_code: HTTP status code (default 200)
        message: Optional success message
        
    Returns:
        tuple: (JSON response, status code)
        
    Example:
        return success_response(category.to_dict(), 201, "Category created")
    """
    response = {
        'success': True,
        'data': data
    }
    if message:
        response['message'] = message
    return jsonify(response), status_code


def handle_exceptions(f):
    """
    Decorator to handle exceptions in route handlers.
    
    Catches common exceptions and returns appropriate error responses.
    Use this decorator on all route handlers for consistent error handling.
    
    Usage:
        @category_bp.route('/categories', methods=['GET'])
        @handle_exceptions
        def get_all_categories():
            # Your code here - no need for try/except
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError as e:
            # Custom API errors - already formatted
            return jsonify(e.to_dict()), e.status_code
        except mysql.connector.IntegrityError as e:
            # Database integrity errors (duplicate key, foreign key violation)
            if 'Duplicate entry' in str(e):
                return error_response(
                    "A record with this value already exists",
                    409,
                    "DUPLICATE_ENTRY",
                    {"mysql_error": str(e)}
                )
            elif 'foreign key constraint' in str(e).lower():
                return error_response(
                    "Referenced record does not exist",
                    400,
                    "FOREIGN_KEY_VIOLATION",
                    {"mysql_error": str(e)}
                )
            return error_response(
                "Database integrity error",
                400,
                "INTEGRITY_ERROR",
                {"mysql_error": str(e)}
            )
        except mysql.connector.Error as e:
            # General database errors
            return error_response(
                "Database error occurred",
                500,
                "DATABASE_ERROR",
                {"mysql_error": str(e)}
            )
        except ValueError as e:
            # Value/type conversion errors
            return error_response(
                str(e),
                400,
                "VALIDATION_ERROR"
            )
        except Exception as e:
            # Unexpected errors - log these in production
            return error_response(
                "An unexpected error occurred",
                500,
                "INTERNAL_ERROR",
                {"exception": str(e)}
            )
    return decorated_function


# Predefined error responses for common scenarios
class Errors:
    """Predefined error responses for common scenarios."""
    
    @staticmethod
    def not_found(resource_name, resource_id=None):
        """Resource not found error."""
        message = f"{resource_name} not found"
        if resource_id:
            message = f"{resource_name} with ID {resource_id} not found"
        return error_response(message, 404, "RESOURCE_NOT_FOUND")
    
    @staticmethod
    def validation_failed(errors):
        """
        Validation failed error.
        
        Args:
            errors: List of validation error messages or dict of field errors
        """
        return error_response(
            "Validation failed",
            400,
            "VALIDATION_ERROR",
            errors
        )
    
    @staticmethod
    def missing_field(field_name):
        """Required field missing error."""
        return error_response(
            f"Missing required field: {field_name}",
            400,
            "MISSING_FIELD",
            {"field": field_name}
        )
    
    @staticmethod
    def invalid_json():
        """Invalid JSON in request body."""
        return error_response(
            "Request body must be valid JSON",
            400,
            "INVALID_JSON"
        )
    
    @staticmethod
    def invalid_type(field_name, expected_type):
        """Field has wrong type."""
        return error_response(
            f"Field '{field_name}' must be {expected_type}",
            400,
            "INVALID_TYPE",
            {"field": field_name, "expected_type": expected_type}
        )