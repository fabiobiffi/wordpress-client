"""
Utility functions for WordPress API client.
"""

from typing import Dict, Optional, Any
from urllib.parse import urljoin, urlencode


def build_api_url(base_url: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Build a complete API URL with optional query parameters.
    
    Args:
        base_url: Base WordPress site URL
        endpoint: API endpoint path
        params: Optional query parameters
        
    Returns:
        Complete URL with query parameters
    """
    base_url = base_url.rstrip('/')
    endpoint = endpoint.lstrip('/')
    
    # Ensure wp-json prefix
    if not endpoint.startswith('wp-json'):
        endpoint = f"wp-json/{endpoint}"
    
    url = urljoin(f"{base_url}/", endpoint)
    
    if params:
        # Remove None values
        filtered_params = {k: v for k, v in params.items() if v is not None}
        if filtered_params:
            query_string = urlencode(filtered_params)
            url = f"{url}?{query_string}"
    
    return url


def sanitize_html(content: str) -> str:
    """
    Basic HTML sanitization for WordPress content.
    
    Args:
        content: HTML content to sanitize
        
    Returns:
        Sanitized content
    """
    # WordPress handles most sanitization, but we can do basic cleanup
    if not content:
        return ""
    
    # Remove null bytes
    content = content.replace('\x00', '')
    
    return content


def format_post_data(title: str, content: str, status: str = "draft", 
                     categories: Optional[list] = None, tags: Optional[list] = None,
                     featured_media: Optional[int] = None) -> Dict[str, Any]:
    """
    Format post data for WordPress API.
    
    Args:
        title: Post title
        content: Post content (HTML)
        status: Post status (draft, publish, private)
        categories: List of category IDs
        tags: List of tag IDs
        featured_media: Featured image ID
        
    Returns:
        Formatted post data dictionary
    """
    data: Dict[str, Any] = {
        "title": title,
        "content": sanitize_html(content),
        "status": status
    }
    
    if categories:
        data["categories"] = categories
    
    if tags:
        data["tags"] = tags
    
    if featured_media:
        data["featured_media"] = featured_media
    
    return data


def parse_wp_error(response_data: dict) -> str:
    """
    Parse WordPress error response and extract message.
    
    Args:
        response_data: Error response from WordPress API
        
    Returns:
        Error message string
    """
    if not isinstance(response_data, dict):
        return "Unknown error occurred"
    
    # WordPress REST API error format
    if "message" in response_data:
        return response_data["message"]
    
    # Check for code and message structure
    if "code" in response_data and "message" in response_data:
        return f"{response_data['code']}: {response_data['message']}"
    
    # Check for data field with additional info
    if "data" in response_data and isinstance(response_data["data"], dict):
        if "message" in response_data["data"]:
            return response_data["data"]["message"]
    
    return "Unknown error occurred"


def validate_status(status: str) -> bool:
    """
    Validate post status value.
    
    Args:
        status: Status string to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_statuses = ["publish", "future", "draft", "pending", "private", "trash"]
    return status in valid_statuses


def chunk_list(items: list, chunk_size: int) -> list:
    """
    Split a list into chunks of specified size.
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunked lists
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
