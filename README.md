# WordPress Client

A modern and easy-to-use Python library for interacting with the WordPress REST API.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Features

- **Complete REST API**: Support for posts, media, users and more
- **Authentication**: Support for Basic Auth and JWT
- **Type hints**: Fully typed for better development experience
- **Error handling**: Custom exceptions for different scenarios
- **Async support**: Support for asynchronous operations (optional)
- **Logging**: Integrated logging system for debugging and monitoring

## 🚀 Quick Installation

### From PyPI (when published)

```bash
pip install wordpress-client
```

### From source

```bash
git clone https://github.com/fabio/wordpress-client.git
cd wordpress-client
pip install -e .
```

## 📖 Basic Usage

### Initial Setup

```python
from wordpress_client import WordPressClient

# Connection with Basic Auth
client = WordPressClient(
    base_url="https://your-wordpress-site.com",
    username="your-username", 
    password="your-password"
)

# Or with JWT (if configured)
client = WordPressClient(
    base_url="https://your-wordpress-site.com",
    jwt_token="your-jwt-token"
)
```

### Posts Management

```python
# Get all posts
posts = client.get_posts()

# Create a new post
new_post = client.create_post({
    'title': 'My new post',
    'content': 'Post content...',
    'status': 'publish'
})

# Update an existing post
updated_post = client.update_post(post_id=123, data={
    'title': 'Updated title'
})

# Delete a post
client.delete_post(post_id=123)
```

### Media Management

```python
# Upload a file
with open('image.jpg', 'rb') as f:
    media = client.upload_media(f, 'image.jpg', 'image/jpeg')

# Get media information
media_info = client.get_media(media_id=456)
```

### Users Management

```python
# Get users
users = client.get_users()

# Create a new user
new_user = client.create_user({
    'username': 'newuser',
    'email': 'user@example.com',
    'password': 'secure-password'
})
```

## 🔧 Building and Compilation

This project uses `hatchling` as build system and can be compiled as a distributable library.

### Prerequisites

```bash
# Install hatchling
pip install hatchling

# Or install all development dependencies
pip install -e ".[dev]"
```

### Library Build

```bash
# Build wheel package and source distribution
python -m build

# Or using hatch directly
hatch build
```

The compiled files will be available in the `dist/` folder:
- `wordpress_client-X.X.X.tar.gz` (source distribution)
- `wordpress_client-X.X.X-py3-none-any.whl` (wheel package)

### Publishing to PyPI

```bash
# Install twine for deployment
pip install twine

# Upload to TestPyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

### Build with custom configuration

```bash
# Build wheel only
python -m build --wheel

# Build source distribution only  
python -m build --sdist

# Build with specific target
hatch build -t wheel
```

## 🧪 Development and Testing

### Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/fabio/wordpress-client.git
cd wordpress-client

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev,test]"
```

### Running Tests

```bash
# All tests
pytest

# Tests with coverage
pytest --cov=wordpress_client --cov-report=html

# Specific tests
pytest tests/test_client.py -v
```

### Code Quality

```bash
# Code formatting
black .

# Import sorting
isort .

# Linting
flake8

# Type checking
mypy .
```

## 📚 Project Structure

```
wordpress-client/
├── __init__.py          # Library entry point
├── auth.py              # Authentication system
├── client.py            # Main client
├── exceptions.py        # Custom exceptions
├── utils.py             # General utilities
├── models/              # Data models
│   ├── media.py         # Media model
│   ├── post.py          # Post model
│   └── user.py          # User model
├── tests/               # Test suite
├── docs/                # Documentation
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## 🛠️ Advanced Configuration

### Timeout and Retry Customization

```python
client = WordPressClient(
    base_url="https://your-site.com",
    username="user",
    password="pass",
    timeout=30,
    max_retries=3,
    retry_delay=1.0
)
```

### Custom Logging

```python
import logging
from wordpress_client import WordPressClient

# Logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wordpress_client')

client = WordPressClient(
    base_url="https://your-site.com",
    username="user", 
    password="pass",
    logger=logger
)
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🐛 Bug Reports & Feature Requests

If you find a bug or have an idea for a new feature, please open an [issue](https://github.com/fabio/wordpress-client/issues).

## 📧 Contact

Fabio - [@fabio](https://github.com/fabio) - fabio@example.com

Project Link: [https://github.com/fabio/wordpress-client](https://github.com/fabio/wordpress-client)

---

⭐️ If this project is useful to you, consider giving it a star on GitHub!