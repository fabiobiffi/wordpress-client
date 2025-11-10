"""
Category model for WordPress API.
"""

from typing import Optional
from pydantic import BaseModel, Field


class Category(BaseModel):
    """
    WordPress Category model.
    
    Represents a WordPress category/taxonomy term.
    """
    id: Optional[int] = None
    count: Optional[int] = Field(default=0, description="Number of posts in category")
    description: Optional[str] = Field(default="", description="Category description")
    link: Optional[str] = None
    name: Optional[str] = Field(description="Category name")
    slug: Optional[str] = None
    taxonomy: Optional[str] = Field(default="category", description="Taxonomy type")
    parent: Optional[int] = Field(default=0, description="Parent category ID")
    meta: Optional[list] = Field(default_factory=list, description="Meta fields")


class CategoryCreate(BaseModel):
    """Model for creating a new category."""
    name: str = Field(description="Category name")
    description: Optional[str] = Field(default=None, description="Category description")
    slug: Optional[str] = Field(default=None, description="Category slug")
    parent: Optional[int] = Field(default=0, description="Parent category ID")


class CategoryUpdate(BaseModel):
    """Model for updating an existing category."""
    name: Optional[str] = Field(default=None, description="Category name")
    description: Optional[str] = Field(default=None, description="Category description")
    slug: Optional[str] = Field(default=None, description="Category slug")
    parent: Optional[int] = Field(default=None, description="Parent category ID")
