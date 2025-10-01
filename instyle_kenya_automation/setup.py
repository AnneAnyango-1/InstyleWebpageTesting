#!/usr/bin/env python3
"""Setup script for Instyle Kenya Test Automation Project"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ {description} failed with exception: {str(e)}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['screenshots', 'reports', 'logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"✓ Created directory: {directory}")
            except Exception as e:
                print(f"✗ Failed to create directory {directory}: {str(e)}")
                return False
        else:
            print(f"✓ Directory already exists: {directory}")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    if not os.path.exists('requirements.txt'):
        print("✗ requirements.txt not found")
        return False
    
    # Upgrade pip first
    pip_upgrade = run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    if not pip_upgrade:
        print("Warning: Could not upgrade pip, continuing anyway...")
    
    # Install requirements
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def check_browsers():
    """Check if supported browsers are installed"""
    print("\nChecking browser availability...")
    
    # Check Chrome
    chrome_commands = {
        'Windows': 'where chrome',
        'Darwin': 'which /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome',
        'Linux': 'which google-chrome || which chromium-browser'
    }
    
    # Check Firefox
    firefox_commands = {
        'Windows': 'where firefox',
        'Darwin': 'which /Applications/Firefox.app/Contents/MacOS/firefox',
        'Linux': 'which firefox'
    }
    
    system = platform.system()
    
    chrome_available = False
    firefox_available = False
    
    # Check Chrome
    if system in chrome_commands:
        try:
            result = subprocess.run(chrome_commands[system], shell=True, capture_output=True)
            if result.returncode == 0:
                chrome_available = True
                print("✓ Chrome browser found")
        except:
            pass
    
    if not chrome_available:
        print("✗ Chrome browser not found")
    
    # Check Firefox
    if system in firefox_commands:
        try:
            result = subprocess.run(firefox_commands[system], shell=True, capture_output=True)
            if result.returncode == 0:
                firefox_available = True
                print("✓ Firefox browser found")
        except:
            pass
    
    if not firefox_available:
        print("✗ Firefox browser not found")
    
    if not chrome_available and not firefox_available:
        print("\n⚠️  Warning: No supported browsers found")
        print("Please install Chrome or Firefox to run tests")
        return False
    
    return True

def run_test_validation():
    """Run a simple test to validate setup"""
    print("\nRunning setup validation test...")
    
    # Create a simple test command
    test_command = f"{sys.executable} -m pytest tests/test_homepage.py::TestHomePage::test_homepage_loads_successfully -v --tb=short"
    
    return run_command(test_command, "Validation test")

def display_usage_instructions():
    """Display usage instructions"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("\n1. Run all tests:")
    print("   pytest")
    print("\n2. Run smoke tests only:")
    print("   pytest -m smoke")
    print("\n3. Run specific test file:")
    print("   pytest tests/test_homepage.py")
    print("\n4. Run with different browser:")
    print("   pytest --browser firefox")
    print("\n5. Generate HTML report:")
    print("   pytest --html=reports/report.html --self-contained-html")
    print("\n6. Run in headless mode:")
    print("   pytest --headless")
    print("\n7. Run tests in parallel:")
    print("   pytest -n 4")
    print("\nFor more information, see README.md")
    print("\nHappy testing! 🚀")

def main():
    """Main setup function"""
    print("Instyle Kenya Test Automation - Setup Script")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n✗ Setup failed during directory creation")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n✗ Setup failed during dependency installation")
        sys.exit(1)
    
    # Check browsers
    browser_check = check_browsers()
    
    # Run validation test (optional)
    if browser_check:
        print("\nWould you like to run a validation test? (y/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['y', 'yes']:
                validation_success = run_test_validation()
                if not validation_success:
                    print("\n⚠️  Validation test failed, but setup is complete")
                    print("You may need to update configuration or check the website")
        except KeyboardInterrupt:
            print("\nSkipping validation test...")
    
    # Display usage instructions
    display_usage_instructions()

if __name__ == "__main__":
    main()
