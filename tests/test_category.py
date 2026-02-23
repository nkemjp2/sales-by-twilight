"""
Unit tests for the Category class.
Tests inheritance, attributes, and methods.
"""

import pytest
import sys
sys.path.insert(0, '.')

from app.models.category import Category
from app.models.base_model import BaseModel
from datetime import datetime


class TestCategoryInheritance:
    """Tests to verify Category inherits from BaseModel."""

    def test_category_inherits_from_base_model(self):
        """Verify that Category is a subclass of BaseModel."""
        assert issubclass(Category, BaseModel)

    def test_category_instance_is_base_model_instance(self):
        """Verify that a Category instance is also a BaseModel instance."""
        category = Category()
        assert isinstance(category, BaseModel)


class TestCategoryInstantiation:
    """Tests for Category instantiation with valid data."""

    def test_category_can_be_instantiated_without_arguments(self):
        """Verify Category can be created with no arguments."""
        category = Category()
        assert category is not None

    def test_category_can_be_instantiated_with_valid_data(self):
        """Verify Category can be created with all arguments."""
        category = Category(
            id=1,
            name="Fresh Produce",
            description="Fruits and vegetables"
        )
        assert category is not None
        assert category.id == 1
        assert category.name == "Fresh Produce"
        assert category.description == "Fruits and vegetables"


class TestCategoryAttributes:
    """Tests to verify Category attributes are set correctly."""

    def test_category_id_is_set_correctly(self):
        """Verify the id attribute is set correctly."""
        category = Category(id=5)
        assert category.id == 5

    def test_category_name_is_set_correctly(self):
        """Verify the name attribute is set correctly."""
        category = Category(name="Dairy & Eggs")
        assert category.name == "Dairy & Eggs"

    def test_category_description_is_set_correctly(self):
        """Verify the description attribute is set correctly."""
        category = Category(description="Milk, cheese, and eggs")
        assert category.description == "Milk, cheese, and eggs"

    def test_category_has_created_at_timestamp(self):
        """Verify Category has created_at from BaseModel."""
        category = Category()
        assert category.created_at is not None
        assert isinstance(category.created_at, datetime)

    def test_category_has_updated_at_timestamp(self):
        """Verify Category has updated_at from BaseModel."""
        category = Category()
        assert category.updated_at is not None
        assert isinstance(category.updated_at, datetime)


class TestCategoryToDict:
    """Tests for the to_dict() method."""

    def test_to_dict_returns_dictionary(self):
        """Verify to_dict() returns a dictionary."""
        category = Category(id=1, name="Beverages")
        result = category.to_dict()
        assert isinstance(result, dict)

    def test_to_dict_contains_all_attributes(self):
        """Verify to_dict() includes all category attributes."""
        category = Category(
            id=1,
            name="Fresh Produce",
            description="Fruits and vegetables"
        )
        result = category.to_dict()
        
        assert "id" in result
        assert "name" in result
        assert "description" in result
        assert "created_at" in result
        assert "updated_at" in result

    def test_to_dict_returns_correct_values(self):
        """Verify to_dict() returns correct attribute values."""
        category = Category(id=2, name="Dairy & Eggs", description="Milk products")
        result = category.to_dict()
        
        assert result["id"] == 2
        assert result["name"] == "Dairy & Eggs"
        assert result["description"] == "Milk products"

    def test_to_dict_converts_datetime_to_string(self):
        """Verify to_dict() converts datetime objects to ISO format strings."""
        category = Category(id=1, name="Test")
        result = category.to_dict()
        
        assert isinstance(result["created_at"], str)
        assert isinstance(result["updated_at"], str)


class TestCategoryRepr:
    """Tests for the __repr__() method."""

    def test_repr_returns_string(self):
        """Verify __repr__() returns a string."""
        category = Category(id=1)
        result = repr(category)
        assert isinstance(result, str)

    def test_repr_contains_class_name(self):
        """Verify __repr__() includes the class name 'Category'."""
        category = Category(id=1)
        result = repr(category)
        assert "Category" in result

    def test_repr_contains_id(self):
        """Verify __repr__() includes the category id."""
        category = Category(id=42)
        result = repr(category)
        assert "42" in result

    def test_repr_format_is_correct(self):
        """Verify __repr__() returns the expected format."""
        category = Category(id=1)
        result = repr(category)
        assert result == "<Category(id=1)>"


class TestCategoryInvalidData:
    """Tests for handling invalid or missing data."""

    def test_category_with_none_values(self):
        """Verify Category handles None values gracefully."""
        category = Category(id=None, name=None, description=None)
        assert category.id is None
        assert category.name is None
        assert category.description is None

    def test_category_to_dict_with_none_values(self):
        """Verify to_dict() works with None values."""
        category = Category(name=None)
        result = category.to_dict()
        assert result["name"] is None