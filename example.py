#!/usr/bin/env python3
"""
Example usage of the WordPress client with the dockerized WordPress instance.
"""
import os
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Load .env file if it exists
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        print(f"📁 Loaded environment from: {env_file}")
    else:
        print("ℹ️  No .env file found, using system environment variables")
except ImportError:
    print("ℹ️  python-dotenv not available, using system environment variables only")

from wordpress_client import WordPressClient


def test_connection(client):
    """Test the WordPress connection."""
    print("Testing WordPress connection...")
    try:
        # Try to make a simple request to check if WordPress is accessible
        client.get_posts(per_page=1)
        print("✅ WordPress connection successful!")
        return True
    except Exception as e:
        print(f"❌ WordPress connection failed: {e}")
        print("💡 Make sure:")
        print("   - Your WordPress site is accessible")
        print("   - REST API is enabled")
        print("   - Your credentials are correct")
        print("   - Application Passwords are set up")
        return False


def main():
    """Main example function."""
    # Get WordPress connection details from environment variables
    wordpress_url = os.getenv('WORDPRESS_URL')
    username = os.getenv('WORDPRESS_USERNAME')
    password = os.getenv('WORDPRESS_PASSWORD')
    
    if not all([wordpress_url, username, password]):
        print("❌ Error: Missing required environment variables!")
        print("💡 Please set the following in your .env file:")
        if not wordpress_url:
            print("   - WORDPRESS_URL (e.g., https://your-site.com)")
        if not username:
            print("   - WORDPRESS_USERNAME")
        if not password:
            print("   - WORDPRESS_PASSWORD (use Application Password from WordPress)")
        print("\n🔑 Create Application Passwords at: WordPress Admin → Users → Profile → Application Passwords")
        sys.exit(1)
    
    print(f"🔗 Connecting to WordPress at: {wordpress_url}")
    print(f"👤 Using username: {username}")
    
    try:
        # Create WordPress client
        client = WordPressClient(
            base_url=wordpress_url,
            username=username,
            password=password
        )
        
        # Test the WordPress connection
        if not test_connection(client):
            print("❌ Could not connect to WordPress. Please check your configuration.")
            sys.exit(1)
        
        print("\n🎉 Successfully connected to WordPress!")
        print("📝 You can now use the WordPress client to interact with your site.")
        print(f"🌐 WordPress admin: {wordpress_url}/wp-admin/")
        print("\nExample usage:")
        print("- Get posts: client.get_posts()")
        print("- Create post: client.create_post({'title': 'My Post', 'content': 'Hello World!'})")
        print("- Get users: client.get_users()")
        
        # Keep the container running
        print("\n🔄 Container is running. Press Ctrl+C to exit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()