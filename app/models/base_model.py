"""
Base Model module for Sales By Twilight API.
Provides common functionality for all entity classes.
"""

from datetime import datetime


class BaseModel:
    """
    Base class that all entity classes will inherit from.
    Provides common attributes and methods.
    """

    def __init__(self, id=None, created_at=None, updated_at=None):
        """
        Initialize base model attributes.
        
        Args:
            id: Unique identifier for the entity
            created_at: Timestamp when entity was created
            updated_at: Timestamp when entity was last updated
        """
        self.id = id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """
        Convert object attributes to dictionary.
        
        Returns:
            dict: Dictionary representation of the object
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    def __repr__(self):
        """
        Return string representation of the object.
        
        Returns:
            str: String representation showing class name and id
        """
        return f"<{self.__class__.__name__}(id={self.id})>"