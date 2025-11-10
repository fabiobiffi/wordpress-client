"""
Media model for WordPress API.
"""

from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class MediaDetails(BaseModel):
    """Media file details."""

    width: Optional[int] = None
    height: Optional[int] = None
    file: Optional[str] = None
    filesize: Optional[int] = None
    sizes: Optional[Dict] = None


class MediaTitle(BaseModel):
    """Media title structure."""

    rendered: Optional[str] = None
    raw: Optional[str] = None


class MediaCaption(BaseModel):
    """Media caption structure."""

    rendered: Optional[str] = None
    raw: Optional[str] = None


class Media(BaseModel):
    """
    WordPress Media model.

    Represents a WordPress media item (image, video, audio, etc.).
    """

    id: Optional[int] = None
    date: Optional[datetime] = None
    date_gmt: Optional[datetime] = None
    modified: Optional[datetime] = None
    modified_gmt: Optional[datetime] = None
    slug: Optional[str] = None
    status: Optional[str] = Field(default="inherit", description="Media status")
    type: Optional[str] = Field(default="attachment", description="Media type")
    link: Optional[str] = None
    title: Optional[MediaTitle] = None
    author: Optional[int] = None
    caption: Optional[MediaCaption] = None
    alt_text: Optional[str] = Field(default="", description="Alternative text")
    media_type: Optional[str] = None
    mime_type: Optional[str] = None
    media_details: Optional[MediaDetails] = None
    post: Optional[int] = Field(default=None, description="Associated post ID")
    source_url: Optional[str] = None

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class MediaUpload(BaseModel):
    """Model for uploading media."""

    file_path: str = Field(description="Local file path to upload")
    title: Optional[str] = Field(default=None, description="Media title")
    alt_text: Optional[str] = Field(default=None, description="Alternative text")
    caption: Optional[str] = Field(default=None, description="Media caption")
    description: Optional[str] = Field(default=None, description="Media description")
    post: Optional[int] = Field(default=None, description="Associated post ID")


class MediaUpdate(BaseModel):
    """Model for updating media metadata."""

    title: Optional[str] = Field(default=None, description="Media title")
    alt_text: Optional[str] = Field(default=None, description="Alternative text")
    caption: Optional[str] = Field(default=None, description="Media caption")
    description: Optional[str] = Field(default=None, description="Media description")
    post: Optional[int] = Field(default=None, description="Associated post ID")
