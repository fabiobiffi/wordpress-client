# WordPress Client

A Python library for interacting with the WordPress REST API.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- CRUD operations for posts, categories, and media
- Application Passwords and JWT authentication
- Command-line interface
- Type-safe with Pydantic models

## Installation

```bash
git clone https://github.com/fabiobiffi/wordpress-client.git
cd wordpress-client
pip install -r requirements.txt
pip install -e .
```

## Configuration

Create a `.env` file:

```env
WP_URL=https://your-wordpress-site.com
WP_USERNAME=your_username
WP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

**Generate Application Password:** WordPress Admin → Users → Profile → Application Passwords

## Quick Start

### Python

```python
from wordpress_client import WordPressClient
from wordpress_client.models.post import PostCreate
import os
from dotenv import load_dotenv

load_dotenv()

client = WordPressClient(
    base_url=os.getenv('WP_URL'),
    username=os.getenv('WP_USERNAME'),
    password=os.getenv('WP_PASSWORD')
)

# Create a post
post = client.create_post(PostCreate(
    title="Hello World",
    content="<p>My first post</p>",
    status="publish"
))

# List posts
posts = client.get_posts(per_page=10)

# Upload media
media = client.upload_media("/path/to/image.jpg", title="My Image")
```

### CLI

```bash
# Create post
python -m wordpress_client.cli post create "Title" "Content" --status publish

# List posts
python -m wordpress_client.cli post list

# Upload media
python -m wordpress_client.cli media upload image.jpg --title "Photo"

# Create category
python -m wordpress_client.cli category create "Technology"
```

## API Reference

### Posts

```python
# Get posts
posts = client.get_posts(per_page=10, status="publish")

# Get single post
post = client.get_post(123)

# Update post
from wordpress_client.models.post import PostUpdate
client.update_post(123, PostUpdate(title="New Title"))

# Delete post
client.delete_post(123, force=True)
```

### Categories

```python
from wordpress_client.models.category import CategoryCreate

# Create category
cat = client.create_category(CategoryCreate(name="Tech"))

# List categories
categories = client.get_categories()

# Delete category
client.delete_category(5, force=True)
```

### Media

```python
# Upload file
media = client.upload_media("/path/to/file.jpg")

# List media
images = client.get_media(media_type="image")

# Delete media
client.delete_media(42, force=True)
```

## Error Handling

```python
from wordpress_client.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError
)

try:
    post = client.get_post(999)
except NotFoundError:
    print("Post not found")
except AuthenticationError:
    print("Authentication failed")
```

## Troubleshooting

**Authentication fails:** Check your Application Password and WordPress URL in `.env`

**Module not found:** Run `pip install -e .` from the project directory

**Connection timeout:** Increase timeout: `WordPressClient(..., timeout=120)`

## Dependencies

- requests
- pydantic
- click
- python-dotenv

## License

MIT License - see [LICENSE](LICENSE) file for details.
