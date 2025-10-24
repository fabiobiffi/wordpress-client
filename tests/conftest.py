"""
Test configuration for WordPress client tests.
"""
import pytest
from pathlib import Path

# Load test environment
test_env = Path(__file__).parent.parent / '.env.test'
if test_env.exists():
    from dotenv import load_dotenv
    load_dotenv(test_env)

@pytest.fixture
def mock_wordpress_config():
    """Mock WordPress configuration for testing."""
    return {
        'base_url': 'https://example.wordpress.com',
        'username': 'testuser',
        'password': 'testpass123',
    }

@pytest.fixture
def mock_response_data():
    """Mock response data for API calls."""
    return {
        'posts': [
            {
                'id': 1,
                'title': {'rendered': 'Test Post'},
                'content': {'rendered': 'Test content'},
                'status': 'publish'
            }
        ],
        'users': [
            {
                'id': 1,
                'name': 'Test User',
                'email': 'test@example.com',
                'roles': ['administrator']
            }
        ]
    }