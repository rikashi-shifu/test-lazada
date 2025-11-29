"""
Setup script for Lazada Test Automation Framework
"""

import os
import sys


def create_directories():
    """Create necessary directories"""
    directories = [
        "src/reports",
        "src/test_data",
        "src/test_data/sensitive",
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# Test Configuration\n")
            f.write("TEST_EMAIL=testuser@example.com\n")
            f.write("TEST_PASSWORD=TestPass123!\n")
            f.write("HEADLESS=False\n")
            f.write("BROWSER=chrome\n")
        print("✓ Created .env file")
    else:
        print("✓ .env file already exists")


def main():
    """Main setup function"""
    print("=" * 80)
    print("LAZADA TEST AUTOMATION FRAMEWORK - SETUP")
    print("=" * 80)
    print()

    print("Creating project directories...")
    create_directories()
    print()

    print("Creating environment file...")
    create_env_file()
    print()

    print("=" * 80)
    print("SETUP COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run tests: python run.py")
    print()


if __name__ == "__main__":
    main()
