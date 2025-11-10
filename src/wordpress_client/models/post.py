"""
Post model for WordPress API.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class PostContent(BaseModel):
    """Post content structure."""
    rendered: Optional[str] = None
    raw: Optional[str] = None


class PostTitle(BaseModel):
    """Post title structure."""
    rendered: Optional[str] = None
    raw: Optional[str] = None


class PostExcerpt(BaseModel):
    """Post excerpt structure."""
    rendered: Optional[str] = None
    raw: Optional[str] = None


class Post(BaseModel):
    """
    WordPress Post model.
    
    Represents a WordPress post with all its properties.
    """
    id: Optional[int] = None
    date: Optional[datetime] = None
    date_gmt: Optional[datetime] = None
    modified: Optional[datetime] = None
    modified_gmt: Optional[datetime] = None
    slug: Optional[str] = None
    status: Optional[str] = Field(default="draft", description="Post status")
    type: Optional[str] = Field(default="post", description="Post type")
    link: Optional[str] = None
    title: Optional[PostTitle] = None
    content: Optional[PostContent] = None
    excerpt: Optional[PostExcerpt] = None
    author: Optional[int] = None
    featured_media: Optional[int] = Field(default=0, description="Featured image ID")
    comment_status: Optional[str] = Field(default="open", description="Comment status")
    ping_status: Optional[str] = Field(default="open", description="Ping status")
    sticky: Optional[bool] = Field(default=False, description="Sticky post")
    template: Optional[str] = Field(default="", description="Template file")
    format: Optional[str] = Field(default="standard", description="Post format")
    categories: Optional[List[int]] = Field(default_factory=list, description="Category IDs")
    tags: Optional[List[int]] = Field(default_factory=list, description="Tag IDs")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class PostCreate(BaseModel):
    """Model for creating a new post."""
    title: str = Field(description="Post title")
    content: str = Field(description="Post content (HTML)")
    status: str = Field(default="draft", description="Post status (draft, publish, private)")
    excerpt: Optional[str] = Field(default=None, description="Post excerpt")
    categories: Optional[List[int]] = Field(default=None, description="Category IDs")
    tags: Optional[List[int]] = Field(default=None, description="Tag IDs")
    featured_media: Optional[int] = Field(default=None, description="Featured image ID")
    author: Optional[int] = Field(default=None, description="Author ID")
    slug: Optional[str] = Field(default=None, description="Post slug")
    format: Optional[str] = Field(default="standard", description="Post format")
    sticky: Optional[bool] = Field(default=False, description="Sticky post")


class PostUpdate(BaseModel):
    """Model for updating an existing post."""
    title: Optional[str] = Field(default=None, description="Post title")
    content: Optional[str] = Field(default=None, description="Post content (HTML)")
    status: Optional[str] = Field(default=None, description="Post status")
    excerpt: Optional[str] = Field(default=None, description="Post excerpt")
    categories: Optional[List[int]] = Field(default=None, description="Category IDs")
    tags: Optional[List[int]] = Field(default=None, description="Tag IDs")
    featured_media: Optional[int] = Field(default=None, description="Featured image ID")
    slug: Optional[str] = Field(default=None, description="Post slug")
    format: Optional[str] = Field(default=None, description="Post format")
    sticky: Optional[bool] = Field(default=None, description="Sticky post")
