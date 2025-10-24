#!/usr/bin/env python3
"""
Test script to verify the WordPress client setup is working correctly.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import requests
        import urllib3
        from pathlib import Path
        
        # Try to load dotenv if available
        try:
            from dotenv import load_dotenv
            print("✅ python-dotenv is available")
        except ImportError:
            print("ℹ️  python-dotenv not available (optional)")
        
        print("✅ All required dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_wordpress_client():
    """Test that the WordPress client can be imported."""
    try:
        from wordpress_client import WordPressClient
        print("✅ WordPress client can be imported")
        return True
    except ImportError as e:
        print(f"❌ Cannot import WordPress client: {e}")
        return False

def test_environment():
    """Test environment setup."""
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file exists")
    else:
        print("ℹ️  .env file not found (optional)")
    
    # Check for required environment variables
    required_vars = ['WORDPRESS_URL', 'WORDPRESS_USERNAME', 'WORDPRESS_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"ℹ️  Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Set these in your .env file to test WordPress connection")
    else:
        print("✅ All required environment variables are set")
    
    return True

def main():
    """Run all tests."""
    print("🧪 Running WordPress Client Setup Tests")
    print("=" * 50)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("WordPress Client", test_wordpress_client),
        ("Environment Setup", test_environment),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print("🎉 All tests passed! Your setup is ready.")
        print("\n📝 Next steps:")
        print("1. Set up your .env file with WordPress credentials")
        print("2. Run: python example.py")
    else:
        print(f"⚠️  {passed}/{total} tests passed. Check the issues above.")
        if not all(results[:2]):  # Critical tests failed
            print("❌ Critical setup issues found. Please fix them before continuing.")
            sys.exit(1)

if __name__ == "__main__":
    main()