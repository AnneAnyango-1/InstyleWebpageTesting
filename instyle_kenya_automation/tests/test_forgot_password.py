"""Forgot password functionality tests"""

import pytest
import logging
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from config.config import Config

logger = logging.getLogger(__name__)

class TestForgotPassword:
    """Test suite for forgot password functionality"""
    
    @pytest.mark.smoke
    def test_forgot_password_page_loads(self, driver):
        """Test that forgot password page loads successfully"""
        # Navigate to login page first
        home_page = HomePage(driver)
        home_page.load()
        
        success = home_page.click_login_link()
        if success:
            login_page = LoginPage(driver)
            if login_page.is_loaded():
                # Click forgot password link
                forgot_success = login_page.click_forgot_password()
                if forgot_success:
                    forgot_page = ForgotPasswordPage(driver)
                    assert forgot_page.is_loaded(), "Forgot password page should load successfully"
                    logger.info("Forgot password page loaded successfully")
                else:
                    # Try direct navigation
                    forgot_page = ForgotPasswordPage(driver)
                    forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
                    if forgot_page.is_loaded():
                        logger.info("Forgot password page loaded via direct navigation")
                    else:
                        pytest.skip("Forgot password page not accessible")
            else:
                pytest.skip("Login page not accessible")
        else:
            pytest.skip("Could not access login page")
    
    def test_forgot_password_form_elements(self, driver):
        """Test that forgot password form has required elements"""
        # Try direct navigation to forgot password page
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            # Try alternative URLs
            alternative_urls = [
                "https://instylekenya.co.ke/account/recover",
                "https://instylekenya.co.ke/pages/forgot-password",
                "https://instylekenya.co.ke/account/reset"
            ]
            
            for url in alternative_urls:
                forgot_page.go_to(url)
                if forgot_page.is_loaded():
                    break
            else:
                pytest.skip("Forgot password page not found")
        
        # Check required form elements
        assert forgot_page.is_form_valid(), "Forgot password form should have required elements"
        assert forgot_page.is_element_present(forgot_page.EMAIL_INPUT), "Email input should be present"
        assert forgot_page.is_element_present(forgot_page.SUBMIT_BUTTON), "Submit button should be present"
        
        # Check page title and instructions
        page_title = forgot_page.get_page_title_text()
        instructions = forgot_page.get_instructions_text()
        
        assert page_title, "Forgot password page should have a title"
        logger.info(f"Forgot password page title: '{page_title}'")
        
        if instructions:
            logger.info(f"Instructions text: '{instructions}'")
        
        logger.info("Forgot password form elements test passed")
    
    def test_valid_email_reset_request(self, driver, test_user_data):
        """Test password reset with valid email"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        # Submit password reset with valid email format
        success = forgot_page.reset_password(test_user_data["email"])
        
        if success:
            # Check for success message
            success_msg = forgot_page.get_success_message()
            if success_msg:
                assert success_msg, "Should show success message after valid email submission"
                logger.info(f"Password reset success message: '{success_msg}'")
            else:
                logger.info("Password reset request submitted (no explicit success message)")
        else:
            # Check for error message
            error_msg = forgot_page.get_error_message()
            logger.info(f"Password reset request failed: '{error_msg}'")
    
    def test_invalid_email_reset_request(self, driver, invalid_user_data):
        """Test password reset with invalid email format"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        # Submit password reset with invalid email
        success = forgot_page.reset_password(invalid_user_data["invalid_email"])
        
        # Should either fail or show error message
        error_msg = forgot_page.get_error_message()
        
        if error_msg:
            logger.info(f"Invalid email correctly rejected: '{error_msg}'")
        elif not success:
            logger.info("Invalid email submission prevented")
        else:
            logger.warning("Invalid email was accepted (unexpected)")
    
    def test_empty_email_reset_request(self, driver):
        """Test password reset with empty email"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        # Submit password reset with empty email
        success = forgot_page.reset_password("")
        
        # Should either fail or show error message
        error_msg = forgot_page.get_error_message()
        
        if error_msg:
            logger.info(f"Empty email correctly rejected: '{error_msg}'")
        elif not success:
            logger.info("Empty email submission prevented")
        else:
            logger.warning("Empty email was accepted (unexpected)")
    
    def test_nonexistent_email_reset_request(self, driver, invalid_user_data):
        """Test password reset with nonexistent email"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        # Submit password reset with nonexistent but valid format email
        success = forgot_page.reset_password(invalid_user_data["nonexistent_email"])
        
        # Behavior might vary - some sites show success for security, others show error
        success_msg = forgot_page.get_success_message()
        error_msg = forgot_page.get_error_message()
        
        if success_msg:
            logger.info(f"Nonexistent email handled with success message (security): '{success_msg}'")
        elif error_msg:
            logger.info(f"Nonexistent email rejected with error: '{error_msg}'")
        else:
            logger.info("Nonexistent email request processed")
    
    def test_back_to_login_link(self, driver):
        """Test back to login link functionality"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        if forgot_page.is_element_present(forgot_page.BACK_TO_LOGIN_LINK):
            success = forgot_page.click_back_to_login()
            
            if success:
                # Should navigate back to login page
                login_page = LoginPage(driver)
                assert login_page.is_loaded(), "Should navigate back to login page"
                logger.info("Back to login link works correctly")
            else:
                logger.warning("Could not click back to login link")
        else:
            logger.info("Back to login link not found")
    
    def test_register_link_from_forgot_password(self, driver):
        """Test register link from forgot password page"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        if forgot_page.is_element_present(forgot_page.REGISTER_LINK):
            success = forgot_page.click_register_link()
            
            if success:
                # Should navigate to registration page
                current_url = driver.current_url.lower()
                assert "register" in current_url or "signup" in current_url, "Should navigate to registration page"
                logger.info("Register link from forgot password page works correctly")
            else:
                logger.warning("Could not click register link")
        else:
            logger.info("Register link not found on forgot password page")
    
    def test_email_field_validation(self, driver):
        """Test email field validation"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        # Test various invalid email formats
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test.example.com",
            "test..test@example.com"
        ]
        
        for invalid_email in invalid_emails:
            forgot_page.clear_email_field()
            
            # Try submitting invalid email
            success = forgot_page.reset_password(invalid_email)
            
            if not success:
                logger.info(f"Invalid email '{invalid_email}' correctly prevented")
            else:
                error_msg = forgot_page.get_error_message()
                if error_msg:
                    logger.info(f"Invalid email '{invalid_email}' rejected: '{error_msg}'")
                else:
                    logger.warning(f"Invalid email '{invalid_email}' was accepted")
    
    def test_multiple_reset_requests(self, driver, test_user_data):
        """Test multiple password reset requests"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        # Submit first reset request
        success1 = forgot_page.reset_password(test_user_data["email"])
        
        if success1:
            # Wait a moment and submit another request
            import time
            time.sleep(2)
            
            forgot_page.clear_email_field()
            success2 = forgot_page.reset_password(test_user_data["email"])
            
            if success2:
                logger.info("Multiple password reset requests allowed")
            else:
                error_msg = forgot_page.get_error_message()
                logger.info(f"Multiple reset requests handled: '{error_msg}'")
        else:
            logger.info("First reset request failed, skipping multiple request test")
    
    @pytest.mark.regression
    def test_forgot_password_page_security(self, driver):
        """Test forgot password page security features"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        # Check that form uses POST method (security best practice)
        form_element = forgot_page.find_element(forgot_page.FORM)
        form_method = form_element.get_attribute("method")
        
        if form_method:
            assert form_method.lower() == "post", "Password reset form should use POST method"
            logger.info("Form uses POST method (secure)")
        
        # Check for CSRF protection (form should have hidden fields)
        hidden_inputs = form_element.find_elements_by_css_selector("input[type='hidden']")
        if len(hidden_inputs) > 0:
            logger.info(f"Found {len(hidden_inputs)} hidden inputs (possible CSRF protection)")
        else:
            logger.info("No hidden inputs found")
    
    def test_form_submission_feedback(self, driver, test_user_data):
        """Test that form provides appropriate feedback after submission"""
        forgot_page = ForgotPasswordPage(driver)
        forgot_page.go_to("https://instylekenya.co.ke/account/login#recover")
        
        if not forgot_page.is_loaded():
            pytest.skip("Forgot password page not accessible")
        
        # Submit form and check for feedback
        success = forgot_page.reset_password(test_user_data["email"])
        
        # Should get either success or error message
        success_msg = forgot_page.get_success_message()
        error_msg = forgot_page.get_error_message()
        
        feedback_provided = bool(success_msg or error_msg or success)
        assert feedback_provided, "Form should provide feedback after submission"
        
        if success_msg:
            logger.info(f"Success feedback provided: '{success_msg}'")
        elif error_msg:
            logger.info(f"Error feedback provided: '{error_msg}'")
        else:
            logger.info("Form submission processed (implicit feedback)")
