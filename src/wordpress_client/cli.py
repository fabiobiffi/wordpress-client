"""
Command Line Interface for WordPress Client.

Provides CLI commands for interacting with WordPress.
"""

import sys
import os
from pathlib import Path
from typing import Optional
import click
from dotenv import load_dotenv

from .client import WordPressClient
from .auth import ApplicationPasswordAuth
from .models.post import PostCreate, PostUpdate
from .models.category import CategoryCreate
from .exceptions import WordPressAPIError

# Load environment variables
load_dotenv()


def get_client() -> WordPressClient:
    """
    Get WordPress client from environment variables.
    
    Required environment variables:
    - WP_URL: WordPress site URL
    - WP_USERNAME: WordPress username
    - WP_PASSWORD: WordPress password or application password
    """
    url = os.getenv('WP_URL')
    username = os.getenv('WP_USERNAME')
    password = os.getenv('WP_PASSWORD')
    
    if not all([url, username, password]):
        click.echo("Error: Missing WordPress credentials in environment variables.", err=True)
        click.echo("Required: WP_URL, WP_USERNAME, WP_PASSWORD", err=True)
        sys.exit(1)
    
    return WordPressClient(
        base_url=url,
        username=username,
        password=password
    )


@click.group()
@click.version_option(version='0.1.0', prog_name='wordpress-client')
def cli():
    """WordPress REST API Client CLI."""
    pass


# ==================== POST COMMANDS ====================

@cli.group()
def post():
    """Manage WordPress posts."""
    pass


@post.command('create')
@click.argument('title')
@click.argument('content')
@click.option('--status', default='draft', help='Post status (draft, publish, private)')
@click.option('--categories', help='Comma-separated category IDs')
@click.option('--tags', help='Comma-separated tag IDs')
def create_post(title: str, content: str, status: str, categories: Optional[str], tags: Optional[str]):
    """Create a new post."""
    try:
        client = get_client()
        
        # Parse categories and tags
        cat_ids = [int(c.strip()) for c in categories.split(',')] if categories else None
        tag_ids = [int(t.strip()) for t in tags.split(',')] if tags else None
        
        post_data = PostCreate(
            title=title,
            content=content,
            status=status,
            categories=cat_ids,
            tags=tag_ids
        )
        
        post = client.create_post(post_data)
        click.echo(f"✓ Post created successfully!")
        click.echo(f"  ID: {post.id}")
        click.echo(f"  Title: {post.title.rendered if post.title else 'N/A'}")
        click.echo(f"  Status: {post.status}")
        click.echo(f"  Link: {post.link}")
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


@post.command('list')
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=10, help='Posts per page')
@click.option('--status', help='Filter by status')
@click.option('--search', help='Search term')
def list_posts(page: int, per_page: int, status: Optional[str], search: Optional[str]):
    """List posts."""
    try:
        client = get_client()
        posts = client.get_posts(page=page, per_page=per_page, status=status, search=search)
        
        if not posts:
            click.echo("No posts found.")
            return
        
        click.echo(f"\nFound {len(posts)} post(s):\n")
        for post in posts:
            title = post.title.rendered if post.title else 'No Title'
            click.echo(f"  [{post.id}] {title}")
            click.echo(f"      Status: {post.status}")
            click.echo(f"      Link: {post.link}")
            click.echo()
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


@post.command('get')
@click.argument('post_id', type=int)
def get_post(post_id: int):
    """Get a single post by ID."""
    try:
        client = get_client()
        post = client.get_post(post_id)
        
        title = post.title.rendered if post.title else 'No Title'
        content = post.content.rendered if post.content else 'No Content'
        
        click.echo(f"\nPost ID: {post.id}")
        click.echo(f"Title: {title}")
        click.echo(f"Status: {post.status}")
        click.echo(f"Link: {post.link}")
        click.echo(f"Date: {post.date}")
        click.echo(f"\nContent:\n{content[:500]}...")
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


@post.command('update')
@click.argument('post_id', type=int)
@click.option('--title', help='New title')
@click.option('--content', help='New content')
@click.option('--status', help='New status')
def update_post(post_id: int, title: Optional[str], content: Optional[str], status: Optional[str]):
    """Update an existing post."""
    try:
        client = get_client()
        
        update_data = PostUpdate(
            title=title,
            content=content,
            status=status
        )
        
        post = client.update_post(post_id, update_data)
        click.echo(f"✓ Post updated successfully!")
        click.echo(f"  ID: {post.id}")
        click.echo(f"  Title: {post.title.rendered if post.title else 'N/A'}")
        click.echo(f"  Status: {post.status}")
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


@post.command('delete')
@click.argument('post_id', type=int)
@click.option('--force', is_flag=True, help='Permanently delete (skip trash)')
@click.confirmation_option(prompt='Are you sure you want to delete this post?')
def delete_post(post_id: int, force: bool):
    """Delete a post."""
    try:
        client = get_client()
        result = client.delete_post(post_id, force=force)
        
        click.echo(f"✓ Post {post_id} deleted successfully!")
        if not force:
            click.echo("  (Moved to trash)")
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


# ==================== CATEGORY COMMANDS ====================

@cli.group()
def category():
    """Manage WordPress categories."""
    pass


@category.command('create')
@click.argument('name')
@click.option('--description', help='Category description')
@click.option('--slug', help='Category slug')
@click.option('--parent', type=int, help='Parent category ID')
def create_category(name: str, description: Optional[str], slug: Optional[str], parent: Optional[int]):
    """Create a new category."""
    try:
        client = get_client()
        
        cat_data = CategoryCreate(
            name=name,
            description=description,
            slug=slug,
            parent=parent or 0
        )
        
        category = client.create_category(cat_data)
        click.echo(f"✓ Category created successfully!")
        click.echo(f"  ID: {category.id}")
        click.echo(f"  Name: {category.name}")
        click.echo(f"  Slug: {category.slug}")
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


@category.command('list')
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=10, help='Categories per page')
@click.option('--search', help='Search term')
def list_categories(page: int, per_page: int, search: Optional[str]):
    """List categories."""
    try:
        client = get_client()
        categories = client.get_categories(page=page, per_page=per_page, search=search)
        
        if not categories:
            click.echo("No categories found.")
            return
        
        click.echo(f"\nFound {len(categories)} category/categories:\n")
        for cat in categories:
            click.echo(f"  [{cat.id}] {cat.name}")
            click.echo(f"      Slug: {cat.slug}")
            click.echo(f"      Count: {cat.count} post(s)")
            click.echo()
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


@category.command('delete')
@click.argument('category_id', type=int)
@click.option('--force', is_flag=True, help='Permanently delete')
@click.confirmation_option(prompt='Are you sure you want to delete this category?')
def delete_category(category_id: int, force: bool):
    """Delete a category."""
    try:
        client = get_client()
        result = client.delete_category(category_id, force=force)
        
        click.echo(f"✓ Category {category_id} deleted successfully!")
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


# ==================== MEDIA COMMANDS ====================

@cli.group()
def media():
    """Manage WordPress media."""
    pass


@media.command('upload')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--title', help='Media title')
@click.option('--alt-text', help='Alternative text')
@click.option('--caption', help='Media caption')
@click.option('--post-id', type=int, help='Associated post ID')
def upload_media(file_path: str, title: Optional[str], alt_text: Optional[str], 
                 caption: Optional[str], post_id: Optional[int]):
    """Upload a media file."""
    try:
        client = get_client()
        
        click.echo(f"Uploading {file_path}...")
        media = client.upload_media(
            file_path=file_path,
            title=title,
            alt_text=alt_text,
            caption=caption,
            post_id=post_id
        )
        
        click.echo(f"✓ Media uploaded successfully!")
        click.echo(f"  ID: {media.id}")
        click.echo(f"  Title: {media.title.rendered if media.title else 'N/A'}")
        click.echo(f"  URL: {media.source_url}")
        click.echo(f"  Type: {media.mime_type}")
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


@media.command('list')
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=10, help='Items per page')
@click.option('--search', help='Search term')
@click.option('--media-type', help='Filter by media type (image, video, audio)')
def list_media(page: int, per_page: int, search: Optional[str], media_type: Optional[str]):
    """List media items."""
    try:
        client = get_client()
        items = client.get_media(page=page, per_page=per_page, search=search, media_type=media_type)
        
        if not items:
            click.echo("No media items found.")
            return
        
        click.echo(f"\nFound {len(items)} media item(s):\n")
        for item in items:
            title = item.title.rendered if item.title else 'No Title'
            click.echo(f"  [{item.id}] {title}")
            click.echo(f"      Type: {item.mime_type}")
            click.echo(f"      URL: {item.source_url}")
            click.echo()
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


@media.command('delete')
@click.argument('media_id', type=int)
@click.option('--force', is_flag=True, help='Permanently delete')
@click.confirmation_option(prompt='Are you sure you want to delete this media item?')
def delete_media(media_id: int, force: bool):
    """Delete a media item."""
    try:
        client = get_client()
        result = client.delete_media(media_id, force=force)
        
        click.echo(f"✓ Media {media_id} deleted successfully!")
        
    except WordPressAPIError as e:
        click.echo(f"✗ Error: {e.message}", err=True)
        sys.exit(1)


def main():
    """Main entry point for CLI."""
    cli()


if __name__ == '__main__':
    main()
