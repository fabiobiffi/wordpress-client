"""
Authentication module for WordPress REST API.

Supports both Application Passwords and JWT token authentication.
"""

from typing import Optional
import base64
import requests
from .exceptions import AuthenticationError


class AuthBase:
    """Base class for authentication methods."""
    
    def get_auth_headers(self) -> dict:
        """Return authentication headers."""
        raise NotImplementedError


class ApplicationPasswordAuth(AuthBase):
    """
    Authentication using WordPress Application Passwords.
    
    This is the recommended method for WordPress 5.6+
    Requires Application Password to be generated in WordPress.
    """
    
    def __init__(self, username: str, app_password: str):
        """
        Initialize Application Password authentication.
        
        Args:
            username: WordPress username
            app_password: Application password (generated in WordPress)
        """
        self.username = username
        self.app_password = app_password
        self._validate_credentials()
    
    def _validate_credentials(self) -> None:
        """Validate that credentials are provided."""
        if not self.username or not self.app_password:
            raise AuthenticationError("Username and application password are required")
    
    def get_auth_headers(self) -> dict:
        """
        Get authentication headers for Application Password auth.
        
        Returns:
            Dictionary with Authorization header
        """
        credentials = f"{self.username}:{self.app_password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded}"
        }


class JWTAuth(AuthBase):
    """
    Authentication using JWT tokens.
    
    Requires JWT Authentication for WP REST API plugin.
    https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/
    """
    
    def __init__(self, base_url: str, username: str, password: str, token: Optional[str] = None):
        """
        Initialize JWT authentication.
        
        Args:
            base_url: WordPress site base URL
            username: WordPress username
            password: WordPress password
            token: Pre-existing JWT token (optional)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = token
        
        if not self.token:
            self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate and get JWT token."""
        url = f"{self.base_url}/wp-json/jwt-auth/v1/token"
        
        try:
            response = requests.post(url, json={
                "username": self.username,
                "password": self.password
            })
            response.raise_for_status()
            data = response.json()
            self.token = data.get("token")
            
            if not self.token:
                raise AuthenticationError("No token received from server")
                
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Failed to authenticate: {str(e)}")
    
    def get_auth_headers(self) -> dict:
        """
        Get authentication headers for JWT auth.
        
        Returns:
            Dictionary with Authorization header
        """
        if not self.token:
            self._authenticate()
        
        return {
            "Authorization": f"Bearer {self.token}"
        }
    
    def validate_token(self) -> bool:
        """
        Validate the current JWT token.
        
        Returns:
            True if token is valid, False otherwise
        """
        if not self.token:
            return False
        
        url = f"{self.base_url}/wp-json/jwt-auth/v1/token/validate"
        headers = self.get_auth_headers()
        
        try:
            response = requests.post(url, headers=headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def refresh_token(self) -> None:
        """Refresh the JWT token by re-authenticating."""
        self._authenticate()
