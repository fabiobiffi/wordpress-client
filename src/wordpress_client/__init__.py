"""
WordPress Client - A Python library for interacting with the WordPress REST API.

This library provides a clean and easy-to-use interface for interacting with
WordPress sites through the REST API.
"""

from .client import WordPressClient
from .exceptions import (
    WordPressAPIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
)

__version__ = "0.1.0"
__author__ = "Fabio Biffi"
__email__ = "fabio@example.com"

__all__ = [
    "WordPressClient",
    "WordPressAPIError",
    "AuthenticationError", 
    "NotFoundError",
    "ValidationError",
]