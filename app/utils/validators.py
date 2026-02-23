"""
Input Validation Module for Sales By Twilight API.

This module provides comprehensive input validation for API requests.
Validates types, ranges, formats, and business rules.
"""

import re
from decimal import Decimal, InvalidOperation


class ValidationError(Exception):
    """Raised when validation fails."""
    
    def __init__(self, errors):
        """
        Initialize with validation errors.
        
        Args:
            errors: List of error messages or dict of field: error pairs
        """
        self.errors = errors
        super().__init__(str(errors))


class Validator:
    """
    Fluent validator for request data.
    
    Usage:
        validator = Validator(data)
        validator.require('name').string('name').max_length('name', 100)
        validator.require('price').positive_decimal('price')
        validator.optional('category_id').positive_integer('category_id')
        
        if not validator.is_valid():
            return Errors.validation_failed(validator.errors)
        
        clean_data = validator.validated_data
    """
    
    def __init__(self, data):
        """
        Initialize validator with request data.
        
        Args:
            data: Dictionary of request data (from request.get_json())
        """
        self.data = data or {}
        self.errors = {}
        self.validated_data = {}
        self._current_field = None
        self._skip_current = False
    
    def require(self, field):
        """
        Mark a field as required.
        
        Args:
            field: Field name
            
        Returns:
            self: For method chaining
        """
        self._current_field = field
        self._skip_current = False
        
        if field not in self.data or self.data[field] is None:
            self._add_error(field, f"'{field}' is required")
            self._skip_current = True
        elif isinstance(self.data[field], str) and not self.data[field].strip():
            self._add_error(field, f"'{field}' cannot be empty")
            self._skip_current = True
        else:
            self.validated_data[field] = self.data[field]
        
        return self
    
    def optional(self, field, default=None):
        """
        Mark a field as optional.
        
        Args:
            field: Field name
            default: Default value if not provided
            
        Returns:
            self: For method chaining
        """
        self._current_field = field
        self._skip_current = False
        
        if field not in self.data or self.data[field] is None:
            self.validated_data[field] = default
            self._skip_current = True
        else:
            self.validated_data[field] = self.data[field]
        
        return self
    
    def string(self, field=None):
        """
        Validate field is a string.
        
        Args:
            field: Field name (uses current field if None)
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        if self._should_skip(field):
            return self
        
        value = self.validated_data.get(field)
        if not isinstance(value, str):
            self._add_error(field, f"'{field}' must be a string")
        else:
            # Strip whitespace from strings
            self.validated_data[field] = value.strip()
        
        return self
    
    def integer(self, field=None):
        """
        Validate field is an integer.
        
        Args:
            field: Field name (uses current field if None)
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        if self._should_skip(field):
            return self
        
        value = self.validated_data.get(field)
        if isinstance(value, bool):
            self._add_error(field, f"'{field}' must be an integer")
        elif isinstance(value, int):
            pass  # Already an integer
        elif isinstance(value, str):
            try:
                self.validated_data[field] = int(value)
            except ValueError:
                self._add_error(field, f"'{field}' must be an integer")
        else:
            self._add_error(field, f"'{field}' must be an integer")
        
        return self
    
    def positive_integer(self, field=None):
        """
        Validate field is a positive integer (> 0).
        
        Args:
            field: Field name (uses current field if None)
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        self.integer(field)
        
        if field not in self.errors:
            value = self.validated_data.get(field)
            if value is not None and value <= 0:
                self._add_error(field, f"'{field}' must be a positive integer")
        
        return self
    
    def non_negative_integer(self, field=None):
        """
        Validate field is a non-negative integer (>= 0).
        
        Args:
            field: Field name (uses current field if None)
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        self.integer(field)
        
        if field not in self.errors:
            value = self.validated_data.get(field)
            if value is not None and value < 0:
                self._add_error(field, f"'{field}' must be zero or greater")
        
        return self
    
    def decimal(self, field=None, max_digits=10, decimal_places=2):
        """
        Validate field is a decimal number.
        
        Args:
            field: Field name (uses current field if None)
            max_digits: Maximum total digits
            decimal_places: Maximum decimal places
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        if self._should_skip(field):
            return self
        
        value = self.validated_data.get(field)
        
        try:
            if isinstance(value, (int, float)):
                decimal_value = Decimal(str(value))
            elif isinstance(value, str):
                decimal_value = Decimal(value)
            elif isinstance(value, Decimal):
                decimal_value = value
            else:
                self._add_error(field, f"'{field}' must be a number")
                return self
            
            # Round to specified decimal places
            decimal_value = round(decimal_value, decimal_places)
            self.validated_data[field] = float(decimal_value)
            
        except InvalidOperation:
            self._add_error(field, f"'{field}' must be a valid number")
        
        return self
    
    def positive_decimal(self, field=None):
        """
        Validate field is a positive decimal (> 0).
        
        Args:
            field: Field name (uses current field if None)
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        self.decimal(field)
        
        if field not in self.errors:
            value = self.validated_data.get(field)
            if value is not None and value <= 0:
                self._add_error(field, f"'{field}' must be greater than zero")
        
        return self
    
    def non_negative_decimal(self, field=None):
        """
        Validate field is a non-negative decimal (>= 0).
        
        Args:
            field: Field name (uses current field if None)
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        self.decimal(field)
        
        if field not in self.errors:
            value = self.validated_data.get(field)
            if value is not None and value < 0:
                self._add_error(field, f"'{field}' must be zero or greater")
        
        return self
    
    def max_length(self, field=None, max_len=255):
        """
        Validate string field maximum length.
        
        Args:
            field: Field name (uses current field if None)
            max_len: Maximum allowed length
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        if self._should_skip(field):
            return self
        
        value = self.validated_data.get(field)
        if isinstance(value, str) and len(value) > max_len:
            self._add_error(field, f"'{field}' must not exceed {max_len} characters")
        
        return self
    
    def min_length(self, field=None, min_len=1):
        """
        Validate string field minimum length.
        
        Args:
            field: Field name (uses current field if None)
            min_len: Minimum required length
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        if self._should_skip(field):
            return self
        
        value = self.validated_data.get(field)
        if isinstance(value, str) and len(value) < min_len:
            self._add_error(field, f"'{field}' must be at least {min_len} characters")
        
        return self
    
    def in_list(self, field=None, allowed_values=None):
        """
        Validate field value is in a list of allowed values.
        
        Args:
            field: Field name (uses current field if None)
            allowed_values: List of allowed values
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        if self._should_skip(field):
            return self
        
        value = self.validated_data.get(field)
        if allowed_values and value not in allowed_values:
            self._add_error(
                field, 
                f"'{field}' must be one of: {', '.join(str(v) for v in allowed_values)}"
            )
        
        return self
    
    def email(self, field=None):
        """
        Validate field is a valid email address.
        
        Args:
            field: Field name (uses current field if None)
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        if self._should_skip(field):
            return self
        
        value = self.validated_data.get(field)
        if isinstance(value, str):
            # Basic email regex pattern
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, value):
                self._add_error(field, f"'{field}' must be a valid email address")
        
        return self
    
    def phone(self, field=None):
        """
        Validate field is a valid phone number (basic validation).
        
        Args:
            field: Field name (uses current field if None)
            
        Returns:
            self: For method chaining
        """
        field = field or self._current_field
        if self._should_skip(field):
            return self
        
        value = self.validated_data.get(field)
        if isinstance(value, str):
            # Remove common formatting characters
            cleaned = re.sub(r'[\s\-\(\)\.]', '', value)
            # Check if remaining characters are digits (optionally starting with +)
            if not re.match(r'^\+?\d{7,15}$', cleaned):
                self._add_error(field, f"'{field}' must be a valid phone number")
        
        return self
    
    def _should_skip(self, field):
        """Check if validation should be skipped for this field."""
        return self._skip_current and field == self._current_field
    
    def _add_error(self, field, message):
        """Add an error message for a field."""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
    
    def is_valid(self):
        """
        Check if all validations passed.
        
        Returns:
            bool: True if no errors, False otherwise
        """
        return len(self.errors) == 0
    
    def get_errors(self):
        """
        Get all validation errors.
        
        Returns:
            dict: Field names mapped to lists of error messages
        """
        return self.errors


def validate_category_create(data):
    """
    Validate data for creating a category.
    
    Args:
        data: Request data dictionary
        
    Returns:
        tuple: (is_valid, validated_data or errors)
    """
    validator = Validator(data)
    validator.require('name').string().max_length(field='name', max_len=100)
    validator.optional('description').string().max_length(field='description', max_len=500)
    
    if validator.is_valid():
        return True, validator.validated_data
    return False, validator.errors


def validate_category_update(data):
    """
    Validate data for updating a category.
    
    Args:
        data: Request data dictionary
        
    Returns:
        tuple: (is_valid, validated_data or errors)
    """
    validator = Validator(data)
    validator.optional('name').string().max_length(field='name', max_len=100)
    validator.optional('description').string().max_length(field='description', max_len=500)
    
    # At least one field must be provided
    if validator.is_valid():
        if not any(v is not None for v in validator.validated_data.values()):
            return False, {'_general': ['At least one field must be provided']}
        return True, validator.validated_data
    return False, validator.errors


def validate_product_create(data):
    """
    Validate data for creating a product.
    
    Args:
        data: Request data dictionary
        
    Returns:
        tuple: (is_valid, validated_data or errors)
    """
    validator = Validator(data)
    validator.require('name').string().max_length(field='name', max_len=200)
    validator.optional('description').string().max_length(field='description', max_len=1000)
    validator.require('price').positive_decimal()
    validator.optional('stock_quantity', default=0).non_negative_integer()
    validator.optional('category_id').positive_integer()
    
    if validator.is_valid():
        return True, validator.validated_data
    return False, validator.errors


def validate_product_update(data):
    """
    Validate data for updating a product.
    
    Args:
        data: Request data dictionary
        
    Returns:
        tuple: (is_valid, validated_data or errors)
    """
    validator = Validator(data)
    validator.optional('name').string().max_length(field='name', max_len=200)
    validator.optional('description').string().max_length(field='description', max_len=1000)
    validator.optional('price').positive_decimal()
    validator.optional('stock_quantity').non_negative_integer()
    validator.optional('category_id').positive_integer()
    
    if validator.is_valid():
        if not any(v is not None for v in validator.validated_data.values()):
            return False, {'_general': ['At least one field must be provided']}
        return True, validator.validated_data
    return False, validator.errors


def validate_customer_create(data):
    """
    Validate data for creating a customer.
    
    Args:
        data: Request data dictionary
        
    Returns:
        tuple: (is_valid, validated_data or errors)
    """
    validator = Validator(data)
    validator.require('first_name').string().max_length(field='first_name', max_len=50)
    validator.require('last_name').string().max_length(field='last_name', max_len=50)
    validator.require('email').string().email().max_length(field='email', max_len=100)
    validator.optional('phone').string().phone().max_length(field='phone', max_len=20)
    
    if validator.is_valid():
        return True, validator.validated_data
    return False, validator.errors


def validate_order_create(data):
    """
    Validate data for creating an order.
    
    Args:
        data: Request data dictionary
        
    Returns:
        tuple: (is_valid, validated_data or errors)
    """
    validator = Validator(data)
    validator.require('customer_id').positive_integer()
    
    # Validate items array
    if 'items' not in data or not isinstance(data.get('items'), list):
        validator.errors['items'] = ['items must be a non-empty array']
    elif len(data['items']) == 0:
        validator.errors['items'] = ['Order must contain at least one item']
    else:
        items_errors = []
        validated_items = []
        for i, item in enumerate(data['items']):
            item_validator = Validator(item)
            item_validator.require('product_id').positive_integer()
            item_validator.require('quantity').positive_integer()
            
            if not item_validator.is_valid():
                items_errors.append({f'item_{i}': item_validator.errors})
            else:
                validated_items.append(item_validator.validated_data)
        
        if items_errors:
            validator.errors['items'] = items_errors
        else:
            validator.validated_data['items'] = validated_items
    
    if validator.is_valid():
        return True, validator.validated_data
    return False, validator.errors


ORDER_STATUSES = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']


def validate_order_status_update(data):
    """
    Validate data for updating order status.
    
    Args:
        data: Request data dictionary
        
    Returns:
        tuple: (is_valid, validated_data or errors)
    """
    validator = Validator(data)
    validator.require('status').string().in_list(field='status', allowed_values=ORDER_STATUSES)
    
    if validator.is_valid():
        return True, validator.validated_data
    return False, validator.errors