"""
Tests for the WordPress client core functionality.
"""
import pytest
from unittest.mock import Mock, patch

from wordpress_client import WordPressClient
from wordpress_client.exceptions import WordPressAPIError


class TestWordPressClient:
    """Test cases for WordPressClient class."""
    
    def test_client_initialization(self, mock_wordpress_config):
        """Test client can be initialized with valid config."""
        client = WordPressClient(
            base_url=mock_wordpress_config['base_url'],
            username=mock_wordpress_config['username'],
            password=mock_wordpress_config['password']
        )
        
        assert client.base_url == mock_wordpress_config['base_url']
        assert client.username == mock_wordpress_config['username']
        assert client.password == mock_wordpress_config['password']
    
    def test_client_initialization_missing_params(self):
        """Test client initialization fails with missing parameters."""
        with pytest.raises(ValueError):
            WordPressClient(base_url="https://example.com")
    
    @patch('requests.get')
    def test_get_posts_success(self, mock_get, mock_wordpress_config, mock_response_data):
        """Test successful posts retrieval."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data['posts']
        mock_get.return_value = mock_response
        
        # Create client and test
        client = WordPressClient(**mock_wordpress_config)
        posts = client.get_posts()
        
        assert len(posts) == 1
        assert posts[0]['title']['rendered'] == 'Test Post'
        
    @patch('requests.get')
    def test_get_posts_api_error(self, mock_get, mock_wordpress_config):
        """Test API error handling for posts retrieval."""
        # Setup mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'message': 'Not found'}
        mock_get.return_value = mock_response
        
        # Create client and test
        client = WordPressClient(**mock_wordpress_config)
        
        with pytest.raises(WordPressAPIError):
            client.get_posts()