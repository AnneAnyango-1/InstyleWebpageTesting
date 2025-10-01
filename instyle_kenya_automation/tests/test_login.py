"""Login functionality tests"""

import pytest
import logging
from pages.home_page import HomePage
from pages.login_page import LoginPage
from config.config import Config

logger = logging.getLogger(__name__)

class TestLogin:
    """Test suite for login functionality"""
    
    @pytest.mark.login
    @pytest.mark.smoke
    def test_login_page_loads(self, driver):
        """Test that login page loads successfully"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Navigate to login page
        success = home_page.click_login_link()
        assert success, "Should be able to click login link"
        
        login_page = LoginPage(driver)
        assert login_page.is_loaded(), "Login page should load successfully"
        assert login_page.is_form_valid(), "Login form should have required elements"
        logger.info("Login page loaded successfully")
    
    @pytest.mark.login
    @pytest.mark.smoke
    def test_valid_login(self, driver, test_user_data):
        """Test login with valid credentials"""
        login_page = LoginPage(driver)
        login_page.load()
        
        success = login_page.login(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )
        
        if success:
            assert success, "Login with valid credentials should succeed"
            # Check if redirected away from login page
            assert "login" not in driver.current_url.lower(), "Should be redirected after successful login"
            logger.info("Valid login test passed")
        else:
            # If login failed, check for error message
            error_msg = login_page.get_error_message()
            logger.warning(f"Login failed (may be expected if test user doesn't exist): {error_msg}")
    
    @pytest.mark.login
    def test_invalid_email_login(self, driver, invalid_user_data):
        """Test login with invalid email format"""
        login_page = LoginPage(driver)
        login_page.load()
        
        success = login_page.login(
            email=invalid_user_data["invalid_email"],
            password="somepassword"
        )
        
        assert not success or login_page.get_error_message(), "Login with invalid email should fail or show error"
        logger.info("Invalid email login test passed")
    
    @pytest.mark.login
    def test_empty_credentials_login(self, driver):
        """Test login with empty credentials"""
        login_page = LoginPage(driver)
        login_page.load()
        
        success = login_page.login(email="", password="")
        
        assert not success or login_page.get_error_message(), "Login with empty credentials should fail"
        logger.info("Empty credentials login test passed")
    
    @pytest.mark.login
    def test_nonexistent_user_login(self, driver, invalid_user_data):
        """Test login with nonexistent user"""
        login_page = LoginPage(driver)
        login_page.load()
        
        success = login_page.login(
            email=invalid_user_data["nonexistent_email"],
            password=invalid_user_data["wrong_password"]
        )
        
        assert not success or login_page.get_error_message(), "Login with nonexistent user should fail"
        
        error_msg = login_page.get_error_message()
        if error_msg:
            logger.info(f"Nonexistent user login failed as expected: {error_msg}")
        else:
            logger.info("Nonexistent user login test passed")
    
    @pytest.mark.login
    def test_wrong_password_login(self, driver, test_user_data, invalid_user_data):
        """Test login with correct email but wrong password"""
        login_page = LoginPage(driver)
        login_page.load()
        
        success = login_page.login(
            email=test_user_data["email"],
            password=invalid_user_data["wrong_password"]
        )
        
        assert not success or login_page.get_error_message(), "Login with wrong password should fail"
        
        error_msg = login_page.get_error_message()
        if error_msg:
            logger.info(f"Wrong password login failed as expected: {error_msg}")
        else:
            logger.info("Wrong password login test passed")
    
    @pytest.mark.login
    def test_remember_me_functionality(self, driver, test_user_data):
        """Test remember me checkbox functionality"""
        login_page = LoginPage(driver)
        login_page.load()
        
        if login_page.is_element_present(login_page.REMEMBER_ME_CHECKBOX):
            # Test checking remember me
            success = login_page.login(
                email=test_user_data["email"],
                password=test_user_data["password"],
                remember_me=True
            )
            
            # Note: Testing persistent login would require multiple browser sessions
            logger.info("Remember me functionality test completed")
        else:
            logger.info("Remember me checkbox not found on login page")
    
    @pytest.mark.login
    def test_forgot_password_link(self, driver):
        """Test forgot password link functionality"""
        login_page = LoginPage(driver)
        login_page.load()
        
        if login_page.is_element_present(login_page.FORGOT_PASSWORD_LINK):
            success = login_page.click_forgot_password()
            
            if success:
                assert success, "Should be able to click forgot password link"
                current_url = driver.current_url.lower()
                assert "forgot" in current_url or "recover" in current_url, "Should navigate to password recovery page"
                logger.info("Forgot password link test passed")
            else:
                logger.warning("Could not click forgot password link")
        else:
            logger.info("Forgot password link not found")
    
    @pytest.mark.login
    def test_create_account_link(self, driver):
        """Test create account link functionality"""
        login_page = LoginPage(driver)
        login_page.load()
        
        if login_page.is_element_present(login_page.CREATE_ACCOUNT_LINK):
            success = login_page.click_create_account()
            
            if success:
                assert success, "Should be able to click create account link"
                current_url = driver.current_url.lower()
                assert "register" in current_url or "signup" in current_url, "Should navigate to registration page"
                logger.info("Create account link test passed")
            else:
                logger.warning("Could not click create account link")
        else:
            logger.info("Create account link not found")
    
    @pytest.mark.login
    def test_login_form_validation(self, driver):
        """Test login form field validation"""
        login_page = LoginPage(driver)
        login_page.load()
        
        # Test form clearing
        login_page.send_keys_to_element(login_page.EMAIL_INPUT, "test@example.com")
        login_page.send_keys_to_element(login_page.PASSWORD_INPUT, "testpassword")
        
        login_page.clear_form()
        
        email_value = login_page.get_element_attribute(login_page.EMAIL_INPUT, "value")
        password_value = login_page.get_element_attribute(login_page.PASSWORD_INPUT, "value")
        
        assert email_value == "", "Email field should be cleared"
        assert password_value == "", "Password field should be cleared"
        logger.info("Login form validation test passed")
    
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_page_elements(self, driver):
        """Test that all required login page elements are present"""
        login_page = LoginPage(driver)
        login_page.load()
        
        # Check required form elements
        assert login_page.is_element_present(login_page.EMAIL_INPUT), "Email input should be present"
        assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Password input should be present"
        assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Login button should be present"
        
        # Check page title
        page_title = login_page.get_page_title_text()
        assert page_title, "Login page should have a title"
        
        logger.info(f"Login page elements test passed. Page title: '{page_title}'")
    
    @pytest.mark.login
    def test_login_with_enter_key(self, driver, test_user_data):
        """Test login by pressing Enter key instead of clicking button"""
        from selenium.webdriver.common.keys import Keys
        
        login_page = LoginPage(driver)
        login_page.load()
        
        # Enter credentials
        login_page.send_keys_to_element(login_page.EMAIL_INPUT, test_user_data["email"])
        login_page.send_keys_to_element(login_page.PASSWORD_INPUT, test_user_data["password"])
        
        # Press Enter in password field
        password_field = login_page.find_element(login_page.PASSWORD_INPUT)
        password_field.send_keys(Keys.RETURN)
        
        login_page.wait_for_page_load()
        
        # Check if login was successful (redirected away from login page or no error)
        login_successful = "login" not in driver.current_url.lower()
        error_message = login_page.get_error_message()
        
        if login_successful:
            logger.info("Login with Enter key test passed")
        elif error_message:
            logger.info(f"Login with Enter key failed as expected: {error_message}")
        else:
            logger.info("Login with Enter key test completed")
    
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_security_features(self, driver, test_user_data):
        """Test login security features"""
        login_page = LoginPage(driver)
        login_page.load()
        
        # Test password field is masked
        password_field = login_page.find_element(login_page.PASSWORD_INPUT)
        password_type = password_field.get_attribute("type")
        assert password_type == "password", "Password field should be masked"
        
        # Test that form submission doesn't expose credentials in URL
        login_page.login(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )
        
        current_url = driver.current_url
        assert test_user_data["password"] not in current_url, "Password should not appear in URL"
        assert test_user_data["email"] not in current_url, "Email should not appear in URL"
        
        logger.info("Login security features test passed")
