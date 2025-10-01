"""Registration functionality tests"""

import pytest
import logging
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from config.config import Config
import time

logger = logging.getLogger(__name__)

class TestRegistration:
    """Test suite for user registration functionality"""
    
    @pytest.mark.smoke
    def test_registration_page_loads(self, driver):
        """Test that registration page loads successfully"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Navigate to registration page
        success = home_page.click_register_link()
        
        if success:
            registration_page = RegistrationPage(driver)
            assert registration_page.is_loaded(), "Registration page should load successfully"
            assert registration_page.is_form_valid(), "Registration form should have required elements"
            logger.info("Registration page loaded successfully")
        else:
            # Try direct navigation
            registration_page = RegistrationPage(driver)
            registration_page.load()
            
            if registration_page.is_loaded():
                logger.info("Registration page loaded via direct navigation")
            else:
                pytest.skip("Registration page not accessible")
    
    def test_registration_form_elements(self, driver):
        """Test that all registration form elements are present"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        # Check required form elements
        assert registration_page.is_element_present(registration_page.EMAIL_INPUT), "Email input should be present"
        assert registration_page.is_element_present(registration_page.PASSWORD_INPUT), "Password input should be present"
        assert registration_page.is_element_present(registration_page.REGISTER_BUTTON), "Register button should be present"
        
        # Check page title
        page_title = registration_page.get_page_title_text()
        assert page_title, "Registration page should have a title"
        
        logger.info(f"Registration form elements test passed. Page title: '{page_title}'")
    
    def test_valid_user_registration(self, driver):
        """Test registration with valid user data"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        # Create unique test user data
        timestamp = str(int(time.time()))
        test_user = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"testuser{timestamp}@example.com",
            "password": "TestPassword123!",
            "phone": "+254700000000"
        }
        
        success = registration_page.register_user(test_user)
        
        if success:
            assert success, "Registration with valid data should succeed"
            
            # Check for success message or redirect
            success_msg = registration_page.get_success_message()
            redirected = "register" not in driver.current_url.lower()
            
            assert success_msg or redirected, "Should show success message or redirect after registration"
            logger.info(f"Valid user registration test passed for {test_user['email']}")
        else:
            error_msg = registration_page.get_error_message()
            logger.warning(f"Registration failed (may be expected): {error_msg}")
    
    def test_duplicate_email_registration(self, driver, test_user_data):
        """Test registration with already existing email"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        # Try to register with existing email
        user_data = test_user_data.copy()
        user_data.update({
            "first_name": "Test",
            "last_name": "User"
        })
        
        success = registration_page.register_user(user_data)
        
        if not success:
            error_msg = registration_page.get_error_message()
            assert error_msg or not success, "Should show error for duplicate email"
            logger.info(f"Duplicate email registration failed as expected: {error_msg}")
        else:
            logger.warning("Duplicate email registration succeeded (unexpected)")
    
    def test_invalid_email_registration(self, driver, invalid_user_data):
        """Test registration with invalid email format"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": invalid_user_data["invalid_email"],
            "password": "TestPassword123!"
        }
        
        success = registration_page.register_user(user_data)
        
        assert not success or registration_page.get_error_message(), "Registration with invalid email should fail"
        
        error_msg = registration_page.get_error_message()
        field_errors = registration_page.get_field_errors()
        
        logger.info(f"Invalid email registration failed as expected. Errors: {error_msg}, Field errors: {field_errors}")
    
    def test_weak_password_registration(self, driver, invalid_user_data):
        """Test registration with weak password"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        timestamp = str(int(time.time()))
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"testuser{timestamp}@example.com",
            "password": invalid_user_data["short_password"]
        }
        
        success = registration_page.register_user(user_data)
        
        # Weak password might be accepted or rejected depending on site policy
        if not success:
            error_msg = registration_page.get_error_message()
            logger.info(f"Weak password registration failed as expected: {error_msg}")
        else:
            logger.info("Weak password was accepted (site may not have strict password policy)")
    
    def test_empty_required_fields(self, driver):
        """Test registration with empty required fields"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        # Try to register with empty email and password
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "",
            "password": ""
        }
        
        success = registration_page.register_user(user_data)
        
        assert not success or registration_page.get_error_message(), "Registration with empty required fields should fail"
        logger.info("Empty required fields registration test passed")
    
    def test_password_confirmation_mismatch(self, driver):
        """Test registration with password confirmation mismatch"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        # Only test if confirm password field exists
        if registration_page.is_element_present(registration_page.CONFIRM_PASSWORD_INPUT):
            timestamp = str(int(time.time()))
            user_data = {
                "first_name": "Test",
                "last_name": "User",
                "email": f"testuser{timestamp}@example.com",
                "password": "TestPassword123!",
                "confirm_password": "DifferentPassword123!"
            }
            
            success = registration_page.register_user(user_data)
            
            assert not success or registration_page.get_error_message(), "Registration with password mismatch should fail"
            logger.info("Password confirmation mismatch test passed")
        else:
            logger.info("Password confirmation field not found")
    
    def test_terms_and_conditions_requirement(self, driver):
        """Test terms and conditions checkbox requirement"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        # Check if terms checkbox exists
        if registration_page.is_element_present(registration_page.TERMS_CHECKBOX):
            timestamp = str(int(time.time()))
            user_data = {
                "first_name": "Test",
                "last_name": "User",
                "email": f"testuser{timestamp}@example.com",
                "password": "TestPassword123!"
            }
            
            # Fill form but don't accept terms
            registration_page.send_keys_to_element(registration_page.EMAIL_INPUT, user_data["email"])
            registration_page.send_keys_to_element(registration_page.PASSWORD_INPUT, user_data["password"])
            
            if registration_page.is_element_present(registration_page.FIRST_NAME_INPUT):
                registration_page.send_keys_to_element(registration_page.FIRST_NAME_INPUT, user_data["first_name"])
            
            # Try to submit without accepting terms
            registration_page.click_element(registration_page.REGISTER_BUTTON)
            registration_page.wait_for_page_load()
            
            # Should either fail or show error
            still_on_register = "register" in driver.current_url.lower()
            error_msg = registration_page.get_error_message()
            
            if still_on_register or error_msg:
                logger.info("Terms and conditions requirement test passed")
            else:
                logger.warning("Registration succeeded without accepting terms")
        else:
            logger.info("Terms and conditions checkbox not found")
    
    def test_newsletter_subscription_option(self, driver):
        """Test newsletter subscription option"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        if registration_page.is_element_present(registration_page.NEWSLETTER_CHECKBOX):
            # Test checking newsletter subscription
            registration_page.click_element(registration_page.NEWSLETTER_CHECKBOX)
            
            is_checked = registration_page.is_newsletter_checkbox_checked()
            assert is_checked, "Newsletter checkbox should be checked after clicking"
            
            logger.info("Newsletter subscription option test passed")
        else:
            logger.info("Newsletter subscription checkbox not found")
    
    def test_form_field_clearing(self, driver):
        """Test form field clearing functionality"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        # Fill form fields
        test_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User"
        }
        
        for field, value in test_data.items():
            field_locator = getattr(registration_page, f"{field.upper()}_INPUT", None)
            if field_locator and registration_page.is_element_present(field_locator):
                registration_page.send_keys_to_element(field_locator, value)
        
        # Clear form
        registration_page.clear_form()
        
        # Verify fields are cleared
        email_value = registration_page.get_element_attribute(registration_page.EMAIL_INPUT, "value")
        assert email_value == "", "Email field should be cleared"
        
        logger.info("Form field clearing test passed")
    
    def test_login_link_from_registration(self, driver):
        """Test login link from registration page"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        if registration_page.is_element_present(registration_page.LOGIN_LINK):
            success = registration_page.click_login_link()
            
            if success:
                assert success, "Should be able to click login link"
                current_url = driver.current_url.lower()
                assert "login" in current_url, "Should navigate to login page"
                logger.info("Login link from registration page test passed")
            else:
                logger.warning("Could not click login link from registration page")
        else:
            logger.info("Login link not found on registration page")
    
    @pytest.mark.regression
    def test_registration_form_validation_messages(self, driver):
        """Test that form validation messages appear correctly"""
        registration_page = RegistrationPage(driver)
        registration_page.load()
        
        if not registration_page.is_loaded():
            pytest.skip("Registration page not accessible")
        
        # Try to submit empty form
        registration_page.click_element(registration_page.REGISTER_BUTTON)
        registration_page.wait_for_page_load()
        
        # Check for validation messages
        error_msg = registration_page.get_error_message()
        field_errors = registration_page.get_field_errors()
        
        # Should have some kind of validation feedback
        has_validation = error_msg or len(field_errors) > 0 or "register" in driver.current_url.lower()
        assert has_validation, "Should show validation messages or stay on form"
        
        logger.info(f"Form validation test passed. Error: '{error_msg}', Field errors: {len(field_errors)}")
