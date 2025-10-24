#!/usr/bin/env python3
"""
WordPress Client Setup Script

This script helps you set up the WordPress client development environment.
"""

import sys
import shutil
import subprocess
from pathlib import Path


def print_header(message):
    """Print a formatted header message."""
    print(f"\n{'='*60}")
    print(f"🚀 {message}")
    print(f"{'='*60}")


def print_step(step, message):
    """Print a formatted step message."""
    print(f"\n📋 Step {step}: {message}")


def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")


def print_info(message):
    """Print an info message."""
    print(f"ℹ️  {message}")


def check_docker():
    """Check if Docker and Docker Compose are available."""
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
        subprocess.run(['docker-compose', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def setup_env_file():
    """Set up the .env file from .env.example."""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if not env_example.exists():
        print_error(".env.example file not found!")
        return False
    
    if env_file.exists():
        response = input("📝 .env file already exists. Overwrite? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print_info("Keeping existing .env file")
            return True
    
    shutil.copy(env_example, env_file)
    print_success("Created .env file from .env.example")
    
    print_info("Please edit the .env file and set your WordPress site details:")
    print("   - WORDPRESS_URL (your WordPress site URL)")
    print("   - WORDPRESS_USERNAME (your WordPress username)")
    print("   - WORDPRESS_PASSWORD (Application Password from WordPress)")
    print("   - Other settings as needed")
    
    return True


def main():
    """Main setup function."""
    print_header("WordPress Client Setup")
    
    print("This script will help you set up the WordPress client development environment.")
    print("You can choose between Docker (for Python development) or local Python setup.")
    print("Note: You need to provide your own WordPress installation.")
    
    # Step 1: Choose setup type
    print_step(1, "Choose Setup Type")
    print("1. Docker setup (Python development environment in container)")
    print("2. Local Python setup (install dependencies locally)")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Please enter 1 or 2")
    
    if choice == '1':
        # Docker setup
        print_step(2, "Checking Docker Installation")
        if not check_docker():
            print_error("Docker or Docker Compose not found!")
            print("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
            sys.exit(1)
        print_success("Docker and Docker Compose are available")
        
        print_step(3, "Setting up Environment File")
        if not setup_env_file():
            sys.exit(1)
        
        print_step(4, "Starting Docker Environment")
        print("Building and starting the Python development container...")
        
        try:
            subprocess.run(['docker-compose', 'up', '-d', '--build'], check=True)
            print_success("Docker environment started successfully!")
            
            print_step(5, "Environment Ready!")
            print("🐳 Docker container is ready for development")
            
            print("\n� Next Steps:")
            print("1. Edit .env file with your WordPress site details")
            print("   - WORDPRESS_URL (your WordPress site URL)")
            print("   - WORDPRESS_USERNAME (your WordPress username)")
            print("   - WORDPRESS_PASSWORD (Application Password from WordPress)")
            print("2. Create Application Passwords in your WordPress Admin")
            print("3. Start development: docker-compose up -d")
            print("4. Enter container: docker-compose exec wordpress-client bash")
            print("5. Run example: python example.py")
            
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to build Docker environment: {e}")
            sys.exit(1)
    
    else:
        # Local setup
        print_step(2, "Setting up Local Python Environment")
        
        print_step(3, "Installing Python Dependencies")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], check=True)
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'python-dotenv'], check=True)
            print_success("Python dependencies installed")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install dependencies: {e}")
            sys.exit(1)
        
        print_step(4, "Setting up Environment File")
        if not setup_env_file():
            sys.exit(1)
        
        print_step(5, "Local Setup Complete!")
        print("📝 Next Steps:")
        print("1. Edit .env file with your WordPress site details")
        print("   - WORDPRESS_URL (your WordPress site URL)")
        print("   - WORDPRESS_USERNAME (your WordPress username)")  
        print("   - WORDPRESS_PASSWORD (Application Password from WordPress)")
        print("2. Make sure your WordPress site has REST API enabled")
        print("3. Create Application Passwords in WordPress Admin → Users → Profile")
        print("4. Run: python example.py")
    
    print_header("Setup Complete!")
    print("📚 For more information, see README.md and DOCKER.md")
    print("🐛 If you encounter issues, check the documentation or open an issue")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)