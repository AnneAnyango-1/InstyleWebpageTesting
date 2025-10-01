# Instyle Kenya Test Automation Project

This is a comprehensive Selenium test automation project for https://instylekenya.co.ke/ using the Page Object Model (POM) design pattern with Python and pytest.

## Project Structure

```
instyle_kenya_automation/
├── config/
│   └── config.py                 # Configuration settings
├── pages/
│   ├── __init__.py
│   ├── base_page.py             # Base page class with common methods
│   ├── home_page.py             # Homepage page object
│   ├── login_page.py            # Login page object
│   ├── registration_page.py     # Registration page object
│   ├── cart_page.py             # Shopping cart page object
│   ├── wishlist_page.py         # Wishlist page object
│   ├── product_page.py          # Product details page object
│   ├── search_results_page.py   # Search results page object
│   └── forgot_password_page.py  # Forgot password page object
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration and fixtures
│   ├── test_homepage.py         # Homepage tests
│   ├── test_login.py            # Login functionality tests
│   ├── test_registration.py     # Registration tests
│   ├── test_cart.py             # Shopping cart tests
│   ├── test_wishlist.py         # Wishlist tests
│   ├── test_search.py           # Search functionality tests
│   ├── test_product_page.py     # Product page tests
│   ├── test_forgot_password.py  # Password recovery tests
│   └── test_navigation.py       # Navigation and general tests
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py        # WebDriver creation and configuration
│   └── helpers.py               # Helper functions and utilities
├── screenshots/                 # Screenshot storage (auto-created)
├── reports/                     # Test reports (auto-created)
├── logs/                        # Log files (auto-created)
├── requirements.txt             # Python dependencies
├── pytest.ini                  # Pytest configuration
└── README.md                    # This file
```

## Features

### Test Coverage
- **Homepage**: Loading, navigation, search, featured products, hero section
- **Authentication**: Login, registration, forgot password, form validation
- **Shopping Cart**: Add/remove items, quantity updates, checkout flow
- **Wishlist**: Add/remove items, move to cart, wishlist management
- **Search**: Basic search, filtering, sorting, pagination
- **Product Pages**: Product details, variants, add to cart/wishlist
- **Navigation**: Menu navigation, breadcrumbs, responsive design
- **Error Handling**: Invalid inputs, edge cases, error messages

### Technical Features
- **Page Object Model (POM)**: Clean, maintainable test structure
- **Cross-browser Support**: Chrome, Firefox with WebDriver Manager
- **Responsive Testing**: Mobile and tablet viewport testing
- **Screenshot Capture**: Automatic screenshots on test failures
- **Comprehensive Logging**: Detailed test execution logs
- **Flexible Configuration**: Easy environment and browser switching
- **Parallel Execution**: Support for parallel test runs
- **Rich Reporting**: HTML reports with test results

## Prerequisites

- Python 3.8 or higher
- Chrome or Firefox browser
- Internet connection

## Installation

1. **Clone or download the project**

2. **Navigate to the project directory**
   ```bash
   cd instyle_kenya_automation
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The main configuration is in `config/config.py`. Key settings include:

- **BASE_URL**: The website URL to test
- **DEFAULT_BROWSER**: Default browser (chrome/firefox)
- **TIMEOUTS**: Wait times for elements and page loads
- **TEST_USER**: Test user credentials (update as needed)
- **SEARCH_TERMS**: Keywords for search testing

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_homepage.py

# Run tests with specific markers
pytest -m smoke          # Run smoke tests only
pytest -m regression     # Run regression tests only
pytest -m "login or cart" # Run login or cart tests
```

### Browser Selection

```bash
# Run with Chrome (default)
pytest --browser chrome

# Run with Firefox
pytest --browser firefox

# Run in headless mode
pytest --headless
```

### Parallel Execution

```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n 4  # Run with 4 parallel workers
```

### Generate Reports

```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Generate Allure report (if allure-pytest installed)
pytest --alluredir=reports/allure
allure serve reports/allure
```

### Test Examples

```bash
# Smoke tests (essential functionality)
pytest -m smoke -v

# Login functionality tests
pytest tests/test_login.py -v

# Cart functionality with HTML report
pytest tests/test_cart.py --html=reports/cart_report.html

# Run specific test method
pytest tests/test_homepage.py::TestHomePage::test_homepage_loads_successfully -v
```

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.smoke`: Critical functionality tests
- `@pytest.mark.regression`: Comprehensive test coverage
- `@pytest.mark.login`: Authentication-related tests
- `@pytest.mark.cart`: Shopping cart functionality
- `@pytest.mark.search`: Search and filtering tests
- `@pytest.mark.wishlist`: Wishlist functionality
- `@pytest.mark.product`: Product page tests
- `@pytest.mark.navigation`: Navigation and UI tests

## Test Data Management

Test data is configured in `config/config.py`:

```python
# Update test user credentials
TEST_USER = {
    "email": "your-test-email@example.com",
    "password": "your-test-password",
    "first_name": "Test",
    "last_name": "User",
    "phone": "+254700000000"
}

# Customize search terms
SEARCH_TERMS = [
    "dress",
    "shoes",
    "handbag",
    "jewelry"
]
```

## Troubleshooting

### Common Issues

1. **WebDriver Issues**
   - The project uses WebDriver Manager to automatically download drivers
   - Ensure you have Chrome or Firefox installed
   - Update browser to latest version if issues persist

2. **Element Not Found Errors**
   - Website structure may have changed
   - Update locators in page object files
   - Increase wait times in config if elements load slowly

3. **Login/Registration Tests Failing**
   - Update test user credentials in config
   - Check if CAPTCHA or additional verification is required
   - Some tests expect user to not exist (for negative testing)

4. **Timeout Errors**
   - Increase timeout values in `config/config.py`
   - Check internet connection speed
   - Website may be slow or under maintenance

### Debug Mode

```bash
# Run with maximum verbosity
pytest -v -s --tb=long

# Run single test with debug output
pytest tests/test_homepage.py::TestHomePage::test_homepage_loads_successfully -v -s

# Keep browser open after test (for debugging)
# Add this to test: input("Press Enter to continue...") before driver.quit()
```

## Extending the Framework

### Adding New Page Objects

1. Create new page class in `pages/` directory
2. Inherit from `BasePage`
3. Define locators and methods
4. Follow existing naming conventions

```python
# Example: pages/new_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class NewPage(BasePage):
    # Locators
    SOME_ELEMENT = (By.CSS_SELECTOR, ".some-class")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def some_action(self):
        return self.click_element(self.SOME_ELEMENT)
```

### Adding New Tests

1. Create test file in `tests/` directory
2. Use appropriate markers
3. Follow naming conventions
4. Add proper documentation

```python
# Example: tests/test_new_feature.py
import pytest
from pages.new_page import NewPage

class TestNewFeature:
    @pytest.mark.smoke
    def test_new_functionality(self, driver):
        new_page = NewPage(driver)
        new_page.load()
        assert new_page.some_action()
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add docstrings to all methods
3. Include appropriate test markers
4. Update README for new features
5. Test changes across different browsers

## Best Practices

1. **Page Objects**
   - Keep page objects focused on single pages
   - Use descriptive method and variable names
   - Return boolean values for action methods
   - Include proper error handling

2. **Test Design**
   - Keep tests independent and atomic
   - Use appropriate assertions
   - Clean up test data when necessary
   - Handle expected failures gracefully

3. **Maintenance**
   - Regular updates to locators
   - Review and update test data
   - Monitor test execution times
   - Update dependencies regularly

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review test logs in `test_automation.log`
3. Check screenshots in `screenshots/` folder for failed tests
4. Ensure website structure hasn't changed significantly

## License

This project is for educational and testing purposes. Ensure compliance with the target website's terms of service.
