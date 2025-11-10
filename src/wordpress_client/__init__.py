""""""

WordPress Client - A Python library for interacting with the WordPress REST API.WordPress Client - A Python library for interacting with the WordPress REST API.



This library provides a clean and easy-to-use interface for interacting withThis library provides a clean and easy-to-use interface for interacting with

WordPress sites through the REST API.WordPress sites through the REST API.

""""""



from .client import WordPressClientfrom .client import WordPressClient

from .auth import AuthBase, ApplicationPasswordAuth, JWTAuthfrom .exceptions import (

from .exceptions import (    WordPressAPIError,

    WordPressAPIError,    AuthenticationError,

    AuthenticationError,    NotFoundError,

    NotFoundError,    ValidationError,

    ValidationError,)

    PermissionError,

)__version__ = "0.1.0"

from .models.post import Post, PostCreate, PostUpdate__author__ = "Fabio Biffi"

from .models.media import Media, MediaUpload, MediaUpdate__email__ = "fabio@example.com"

from .models.category import Category, CategoryCreate, CategoryUpdate

__all__ = [

__version__ = "0.1.0"    "WordPressClient",

__author__ = "Fabio Biffi"    "WordPressAPIError",

__email__ = "fabio@example.com"    "AuthenticationError", 

    "NotFoundError",

__all__ = [    "ValidationError",

    # Main client]
    "WordPressClient",
    
    # Authentication
    "AuthBase",
    "ApplicationPasswordAuth",
    "JWTAuth",
    
    # Exceptions
    "WordPressAPIError",
    "AuthenticationError", 
    "NotFoundError",
    "ValidationError",
    "PermissionError",
    
    # Post models
    "Post",
    "PostCreate",
    "PostUpdate",
    
    # Media models
    "Media",
    "MediaUpload",
    "MediaUpdate",
    
    # Category models
    "Category",
    "CategoryCreate",
    "CategoryUpdate",
]
