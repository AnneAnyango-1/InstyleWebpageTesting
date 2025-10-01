#!/usr/bin/env python3
"""Test runner script for Instyle Kenya Test Automation"""

import argparse
import sys
import os
import subprocess
from datetime import datetime

def run_pytest_command(command, description):
    """Run pytest command and handle output"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        # Run the command
        result = subprocess.run(command, shell=True)
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n❌ Test execution interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {str(e)}")
        return False

def get_test_command(args):
    """Build pytest command based on arguments"""
    cmd_parts = ["pytest"]
    
    # Add test path/marker
    if args.smoke:
        cmd_parts.append("-m smoke")
    elif args.regression:
        cmd_parts.append("-m regression")
    elif args.login:
        cmd_parts.append("-m login")
    elif args.cart:
        cmd_parts.append("-m cart")
    elif args.search:
        cmd_parts.append("-m search")
    elif args.wishlist:
        cmd_parts.append("-m wishlist")
    elif args.navigation:
        cmd_parts.append("-m navigation")
    elif args.file:
        cmd_parts.append(f"tests/{args.file}")
    elif args.test:
        cmd_parts.append(args.test)
    
    # Browser selection
    if args.browser:
        cmd_parts.append(f"--browser {args.browser}")
    
    # Headless mode
    if args.headless:
        cmd_parts.append("--headless")
    
    # Parallel execution
    if args.parallel:
        cmd_parts.append(f"-n {args.parallel}")
    
    # Verbosity
    if args.verbose:
        cmd_parts.append("-v")
    
    # Generate reports
    if args.html_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/test_report_{timestamp}.html"
        cmd_parts.append(f"--html={report_file} --self-contained-html")
        print(f"📊 HTML report will be saved to: {report_file}")
    
    if args.allure:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        allure_dir = f"reports/allure_{timestamp}"
        cmd_parts.append(f"--alluredir={allure_dir}")
        print(f"📊 Allure report will be saved to: {allure_dir}")
    
    # Additional pytest options
    if args.tb:
        cmd_parts.append(f"--tb={args.tb}")
    
    if args.lf:
        cmd_parts.append("--lf")
    
    if args.ff:
        cmd_parts.append("--ff")
    
    return " ".join(cmd_parts)

def validate_environment():
    """Validate that the environment is set up correctly"""
    print("🔍 Validating test environment...")
    
    # Check if we're in the right directory
    if not os.path.exists("tests") or not os.path.exists("pages"):
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    # Check if dependencies are installed
    try:
        import selenium
        import pytest
        print("✅ Core dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Create reports directory if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")
        print("📁 Created reports directory")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Test runner for Instyle Kenya Test Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --smoke                    # Run smoke tests
  python run_tests.py --regression --parallel 4  # Run regression tests in parallel
  python run_tests.py --file test_homepage.py    # Run specific test file
  python run_tests.py --login --browser firefox  # Run login tests with Firefox
  python run_tests.py --cart --html-report       # Run cart tests with HTML report
  python run_tests.py --search --headless        # Run search tests in headless mode
        """
    )
    
    # Test selection
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument("--smoke", action="store_true", 
                           help="Run smoke tests (essential functionality)")
    test_group.add_argument("--regression", action="store_true", 
                           help="Run regression tests (comprehensive)")
    test_group.add_argument("--login", action="store_true", 
                           help="Run login/authentication tests")
    test_group.add_argument("--cart", action="store_true", 
                           help="Run shopping cart tests")
    test_group.add_argument("--search", action="store_true", 
                           help="Run search functionality tests")
    test_group.add_argument("--wishlist", action="store_true", 
                           help="Run wishlist functionality tests")
    test_group.add_argument("--navigation", action="store_true", 
                           help="Run navigation and UI tests")
    test_group.add_argument("--file", type=str, 
                           help="Run specific test file (e.g., test_homepage.py)")
    test_group.add_argument("--test", type=str, 
                           help="Run specific test (full pytest path)")
    
    # Browser options
    parser.add_argument("--browser", choices=["chrome", "firefox"], 
                       default="chrome", help="Browser to use (default: chrome)")
    parser.add_argument("--headless", action="store_true", 
                       help="Run tests in headless mode")
    
    # Execution options
    parser.add_argument("--parallel", type=int, metavar="N", 
                       help="Run tests in parallel with N workers")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    
    # Reporting options
    parser.add_argument("--html-report", action="store_true", 
                       help="Generate HTML test report")
    parser.add_argument("--allure", action="store_true", 
                       help="Generate Allure test report")
    
    # Pytest options
    parser.add_argument("--tb", choices=["short", "long", "line", "native"], 
                       default="short", help="Traceback style (default: short)")
    parser.add_argument("--lf", action="store_true", 
                       help="Run last failed tests only")
    parser.add_argument("--ff", action="store_true", 
                       help="Run failed tests first")
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n💡 Tip: Start with --smoke to run essential tests")
        return
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Build and run command
    command = get_test_command(args)
    description = "Test execution"
    
    # Add description based on test type
    if args.smoke:
        description = "Smoke tests (essential functionality)"
    elif args.regression:
        description = "Regression tests (comprehensive)"
    elif args.login:
        description = "Login/Authentication tests"
    elif args.cart:
        description = "Shopping cart tests"
    elif args.search:
        description = "Search functionality tests"
    elif args.wishlist:
        description = "Wishlist functionality tests"
    elif args.navigation:
        description = "Navigation and UI tests"
    elif args.file:
        description = f"Tests from {args.file}"
    elif args.test:
        description = f"Specific test: {args.test}"
    
    print(f"🚀 Starting: {description}")
    print(f"🌐 Browser: {args.browser.title()}")
    if args.headless:
        print("👤 Mode: Headless")
    if args.parallel:
        print(f"⚡ Parallel workers: {args.parallel}")
    
    # Run tests
    success = run_pytest_command(command, description)
    
    if success:
        print("\n✅ Tests completed successfully!")
        
        if args.html_report:
            print("📊 Check the HTML report in the reports/ directory")
        if args.allure:
            print("📊 Generate Allure report with: allure serve reports/allure_*")
            
    else:
        print("\n❌ Tests completed with failures")
        print("📋 Check the detailed output above for failure information")
        print("📸 Screenshots of failures are saved in screenshots/ directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
