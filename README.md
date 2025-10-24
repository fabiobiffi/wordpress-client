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

## 🚀 Installation & Setup

### Quick Start (Recommended)

Use the automated setup script:

```bash
# Clone the repository
git clone https://github.com/fabiobiffi/wordpress-client.git
cd wordpress-client

# Run the setup script
python setup.py
```

The setup script will guide you through:
- Choosing between Docker or local setup
- Installing dependencies
- Setting up environment variables
- Starting the development environment

### Option 1: Docker (Recommended for Development)

Use Docker for the Python development environment:

```bash
# Clone the repository
git clone https://github.com/fabiobiffi/wordpress-client.git
cd wordpress-client

# Copy environment variables template
cp .env.example .env

# Edit .env file with your WordPress site credentials
# Required: WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD

# Start the development container
docker-compose up -d

# Enter the container for development
docker-compose exec wordpress-client bash
```

**Note:** You need to provide your own WordPress installation. The Docker setup only contains the Python development environment.

### Need a WordPress Instance?

If you don't have a WordPress site yet, you can quickly set one up using Docker. Check out this comprehensive guide: [How to Dockerize WordPress](https://www.docker.com/blog/how-to-dockerize-wordpress/).

**Quick WordPress with Docker:**
```bash
# Create a simple WordPress setup
mkdir my-wordpress && cd my-wordpress

# Create docker-compose.yml for WordPress + MySQL
cat > docker-compose.yml << 'EOF'
services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress_data:/var/www/html

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - db_data:/var/lib/mysql

volumes:
  wordpress_data:
  db_data:
EOF

# Start WordPress
docker-compose up -d

# Access at http://localhost:8080
```

Then use `WORDPRESS_URL=http://localhost:8080` in your client configuration.

### Option 2: From PyPI (when published)

```bash
pip install wordpress-client
```

### Option 3: From source

```bash
git clone https://github.com/fabiobiffi/wordpress-client.git
cd wordpress-client
pip install -e .
```

## 🏃‍♂️ Quick Start Guide

### 1. Using Your WordPress Site

Connect to your existing WordPress installation:

```python
import os
from wordpress_client import WordPressClient

# Using environment variables (recommended)
client = WordPressClient(
    base_url=os.getenv('WORDPRESS_URL'),
    username=os.getenv('WORDPRESS_USERNAME'),
    password=os.getenv('WORDPRESS_PASSWORD')  # Use Application Password
)

# Test the connection
posts = client.get_posts()
print(f"Connected! Found {len(posts)} posts.")
```

### 2. Direct Connection

```python
from wordpress_client import WordPressClient

# Connection with Basic Auth
client = WordPressClient(
    base_url="https://your-wordpress-site.com",
    username="your-username", 
    password="your-application-password"  # Use Application Password, not regular password
)
```

### 3. Environment Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file with your WordPress credentials:

```env
WORDPRESS_URL=https://your-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-application-password
```

Then use it in your code:

```python
import os
from dotenv import load_dotenv
from wordpress_client import WordPressClient

load_dotenv()

client = WordPressClient(
    base_url=os.getenv('WORDPRESS_URL'),
    username=os.getenv('WORDPRESS_USERNAME'),
    password=os.getenv('WORDPRESS_PASSWORD')
)
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

## � Development

### Running the Project Locally

#### Option 1: Docker Development Environment

Use Docker for the Python development environment:

```bash
# Build and start the development container
docker-compose up -d

# Enter the container for interactive development
docker-compose exec wordpress-client bash

# Inside the container, you can:
python example.py                                    # Run the example
python tests/test_setup.py                         # Test the setup
python -m pytest tests/                            # Run unit tests
python -m pytest tests/ --cov=src/wordpress_client # Run with coverage
pip install package-name                           # Install additional packages
```

#### Option 2: Local Python Environment

```bash
# Install dependencies locally
pip install -e .
pip install python-dotenv  # For .env support

# Set up environment
cp .env.example .env
# Edit .env file with your WordPress site details

# Install development dependencies (optional)
pip install -e .[dev]

# Set up pre-commit hooks (optional)
pre-commit install

# Run your code
python example.py
```

### Environment Variables

All configuration is managed through environment variables. See `.env.example` for all available options:

| Variable | Description | Required |
|----------|-------------|----------|
| `WORDPRESS_URL` | WordPress site URL | ✅ |
| `WORDPRESS_USERNAME` | WordPress username | ✅ |
| `WORDPRESS_PASSWORD` | Application password | ✅ |
| `WORDPRESS_JWT_TOKEN` | JWT token (alternative to username/password) | |

### Testing with Your WordPress Site

1. **Set up Application Passwords on your WordPress site:**
   - Go to your WordPress Admin → Users → Profile
   - Scroll down to "Application Passwords"
   - Create a new application password
   - Use this password in your `.env` file

2. **Configure your environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your WordPress site details
   ```

3. **Test the connection:**
   ```bash
   # Using Docker
   docker-compose up -d
   docker-compose exec wordpress-client python example.py
   
   # Or locally
   python example.py
   ```

### Project Scripts

Common development tasks:

```bash
# Format code (when black is installed)
docker-compose exec wordpress-client black .

# Type checking (when mypy is installed)  
docker-compose exec wordpress-client mypy .

# Run linting (when flake8 is installed)
docker-compose exec wordpress-client flake8 .

# Install additional development packages
docker-compose exec wordpress-client pip install pytest black mypy flake8
```

## � Docker Development Guide

### Prerequisites

- Docker and Docker Compose installed on your system
- Git (to clone the repository)
- An existing WordPress installation with REST API enabled

### What's Included

The Docker setup provides:

- **Python 3.11** development environment
- **All project dependencies** pre-installed from requirements.txt
- **WordPress client library** installed in development mode
- **Live code sync** - changes to your local files are reflected immediately
- **Isolated environment** - no conflicts with your system Python

### WordPress Site Requirements

You need to provide your own WordPress installation with:

1. **WordPress 5.0+** with REST API enabled (enabled by default)
2. **Application Passwords** set up for authentication
3. **HTTPS recommended** for production use

#### Setting up Application Passwords

1. **Access your WordPress Admin** → Users → Profile
2. **Scroll down to "Application Passwords"**
3. **Create a new application password**:
   - Application Name: "WordPress Client"
   - Click "Add New Application Password"
4. **Copy the generated password** and use it in your `.env` file

### Using the WordPress Client in Docker

#### Interactive Mode

Start an interactive Python shell in the container:

```bash
docker-compose exec wordpress-client python
```

Then use the client:

```python
from wordpress_client import WordPressClient
import os

# Connect to your WordPress site
client = WordPressClient(
    base_url=os.getenv("WORDPRESS_URL"),
    username=os.getenv("WORDPRESS_USERNAME"),
    password=os.getenv("WORDPRESS_PASSWORD")
)

# Test the connection
posts = client.get_posts()
print(f"Found {len(posts)} posts")
```

#### Running Scripts

Create a Python script and run it in the container:

```bash
docker-compose exec wordpress-client python your_script.py
```

#### Development Mode

The current directory is mounted as a volume, so changes to your code are immediately reflected in the container.

### Common Docker Commands

#### View Logs
```bash
# Container logs
docker-compose logs wordpress-client

# Follow logs in real-time
docker-compose logs -f wordpress-client
```

#### Restart Services
```bash
# Restart container
docker-compose restart wordpress-client
```

#### Stop and Remove
```bash
# Stop services (data preserved)
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

#### Update and Rebuild
```bash
# Rebuild the container
docker-compose build wordpress-client

# Restart with rebuild
docker-compose up -d --build
```

### Docker Troubleshooting

#### Container not starting
- Check if Docker is running: `docker --version`
- Check container logs: `docker-compose logs wordpress-client`
- Rebuild container: `docker-compose build --no-cache`

#### Python client connection issues
- Ensure your WordPress site is accessible
- Check if REST API is enabled (test: `your-site.com/wp-json/wp/v2`)
- Verify application passwords are set up correctly
- Check environment variables in `.env` file
- Test connection: `docker-compose exec wordpress-client python example.py`

#### Environment variable issues
- Ensure `.env` file exists and contains required variables
- Check for spaces around `=` in `.env` file (should be `KEY=value`)
- Restart container after changing `.env`: `docker-compose restart`

### Data Persistence

- **Your code**: Mounted from current directory (live updates)
- **Container state**: Rebuilt each time (no persistent data in container)
- **WordPress data**: Stored on your external WordPress installation

### Verifying Your Setup

Use the included test script to verify everything is working:

```bash
# Test the setup
docker-compose exec wordpress-client python tests/test_setup.py
```

This will check:
- ✅ All dependencies are installed
- ✅ WordPress client can be imported  
- ✅ Environment variables are configured

### Production Considerations

This setup is designed for development. For production:

1. **Security**: Change default passwords and use secure authentication
2. **SSL**: Add HTTPS/SSL certificates
3. **Performance**: Use production-optimized images and configurations
4. **Monitoring**: Add logging and monitoring solutions
5. **Backups**: Implement automated backup strategies

## �📚 Project Structure

```
wordpress-client/
├── src/                 # Source code
│   └── wordpress_client/
│       ├── __init__.py  # Package entry point
│       ├── auth.py      # Authentication system
│       ├── client.py    # Main client
│       ├── exceptions.py # Custom exceptions
│       ├── utils.py     # General utilities
│       └── models/      # Data models
│           ├── media.py # Media model
│           ├── post.py  # Post model
│           └── user.py  # User model
├── tests/               # Test suite
│   ├── __init__.py      # Tests package
│   ├── conftest.py      # Test configuration
│   ├── test_client.py   # Client tests
│   └── test_setup.py    # Setup verification tests
├── docs/                # Documentation
├── example.py           # Usage examples
├── setup.py             # Interactive setup script
├── pyproject.toml       # Project configuration
├── requirements.txt     # Dependencies
├── docker-compose.yml   # Docker development setup
├── Dockerfile           # Python dev container
└── README.md            # This file
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