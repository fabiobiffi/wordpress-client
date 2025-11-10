"""
Custom exceptions for WordPress API client.
"""

from typing import Optional


class WordPressAPIError(Exception):
    """Base exception for all WordPress API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(WordPressAPIError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", status_code: int = 401, response: Optional[dict] = None):
        super().__init__(message, status_code, response)


class NotFoundError(WordPressAPIError):
    """Raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found", status_code: int = 404, response: Optional[dict] = None):
        super().__init__(message, status_code, response)


class ValidationError(WordPressAPIError):
    """Raised when request validation fails."""
    
    def __init__(self, message: str = "Validation failed", status_code: int = 400, response: Optional[dict] = None):
        super().__init__(message, status_code, response)


class PermissionError(WordPressAPIError):
    """Raised when the user doesn't have permission to perform an action."""
    
    def __init__(self, message: str = "Permission denied", status_code: int = 403, response: Optional[dict] = None):
        super().__init__(message, status_code, response)
