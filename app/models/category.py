"""
Category Model module for Sales By Twilight API.
"""

from app.models.base_model import BaseModel


class Category(BaseModel):
    """
    Category class that inherits from BaseModel.
    Represents product categories in the e-commerce system.
    """

    def __init__(self, id=None, name=None, description=None, 
                 created_at=None, updated_at=None):
        """
        Initialize Category with its attributes.

        Args:
            id: Unique identifier for the category
            name: Name of the category
            description: Description of the category
            created_at: Timestamp when category was created
            updated_at: Timestamp when category was last updated
        """
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.description = description