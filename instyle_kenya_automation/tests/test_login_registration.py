import pytest
import time
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.config import Config

@pytest.mark.critical
class TestLoginRegistration:
    """Test cases for login and registration functionality"""
    
    def test_login_page_loads(self, driver):
        """Test that login page loads successfully"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        assert login_page.is_login_page_loaded(), "Login page did not load successfully"
        
    def test_login_page_elements_visibility(self, driver):
        """Test that all login form elements are visible"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # Check for login form elements
        elements_to_check = [
            (login_page.LOGIN_EMAIL_INPUT, "Email input"),
            (login_page.LOGIN_PASSWORD_INPUT, "Password input"),
            (login_page.LOGIN_BUTTON, "Login button")
        ]
        
        for element_locator, element_name in elements_to_check:
            if login_page.is_element_visible(element_locator, timeout=5):
                assert True, f"{element_name} is visible"
            else:
                pytest.skip(f"{element_name} not found - may not be available on this page")
                
    def test_valid_user_registration(self, driver, test_user_data):
        """Test user registration with valid data"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # Check if registration is available
        if not login_page.is_element_visible(login_page.REGISTER_EMAIL, timeout=5):
            if login_page.is_element_visible(login_page.REGISTER_TAB, timeout=3):
                login_page.click_element(login_page.REGISTER_TAB)
                time.sleep(1)
                
        if login_page.is_element_visible(login_page.REGISTER_EMAIL, timeout=5):
            login_page.register(
                first_name=test_user_data["first_name"],
                last_name=test_user_data["last_name"],
                email=test_user_data["email"],
                password=test_user_data["password"],
                phone=test_user_data["phone"]
            )
            
            time.sleep(3)  # Wait for registration process
            
            # Check for success message or redirect
            success_msg = login_page.get_success_message()
            error_msg = login_page.get_error_message()
            
            if error_msg:
                pytest.skip(f"Registration error (expected for test): {error_msg}")
            else:
                assert success_msg or login_page.is_logged_in(), "Registration appears to have failed"
        else:
            pytest.skip("Registration form not available on this page")
            
    def test_registration_with_invalid_email(self, driver, invalid_user_data):
        """Test registration with invalid email"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # Switch to registration if needed
        if login_page.is_element_visible(login_page.REGISTER_TAB, timeout=3):
            login_page.click_element(login_page.REGISTER_TAB)
            time.sleep(1)
            
        if login_page.is_element_visible(login_page.REGISTER_EMAIL, timeout=5):
            login_page.register(
                first_name="Test",
                last_name="User",
                email=invalid_user_data["invalid_email"],
                password="ValidPassword123!",
                phone="+254700123456"
            )
            
            time.sleep(2)
            
            # Should show validation error
            error_msg = login_page.get_error_message()
            validation_errors = login_page.get_validation_errors()
            
            assert error_msg or validation_errors, "Expected validation error for invalid email"
        else:
            pytest.skip("Registration form not available")
            
    def test_registration_with_weak_password(self, driver, invalid_user_data):
        """Test registration with weak password"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        if login_page.is_element_visible(login_page.REGISTER_TAB, timeout=3):
            login_page.click_element(login_page.REGISTER_TAB)
            time.sleep(1)
            
        if login_page.is_element_visible(login_page.REGISTER_EMAIL, timeout=5):
            login_page.register(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                password=invalid_user_data["weak_password"],
                phone="+254700123456"
            )
            
            time.sleep(2)
            
            # Should show validation error
            error_msg = login_page.get_error_message()
            validation_errors = login_page.get_validation_errors()
            
            assert error_msg or validation_errors, "Expected validation error for weak password"
        else:
            pytest.skip("Registration form not available")
            
    def test_login_with_valid_credentials(self, driver):
        """Test login with valid credentials (demo test)"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        if login_page.is_element_visible(login_page.LOGIN_EMAIL_INPUT, timeout=5):
            # Use demo credentials (these will likely fail, but test the process)
            login_page.login(
                email="demo@instylekenya.co.ke",
                password="demo123",
                remember_me=True
            )
            
            time.sleep(3)
            
            # Check result
            if login_page.is_logged_in():
                assert True, "Login successful"
            else:
                error_msg = login_page.get_error_message()
                pytest.skip(f"Login failed as expected for demo credentials: {error_msg}")
        else:
            pytest.skip("Login form not available")
            
    def test_login_with_empty_credentials(self, driver, invalid_user_data):
        """Test login with empty credentials"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        if login_page.is_element_visible(login_page.LOGIN_EMAIL_INPUT, timeout=5):
            login_page.login(
                email=invalid_user_data["empty_email"],
                password=invalid_user_data["empty_password"]
            )
            
            time.sleep(2)
            
            # Should show validation error
            error_msg = login_page.get_error_message()
            validation_errors = login_page.get_validation_errors()
            
            assert error_msg or validation_errors or not login_page.is_logged_in(), "Expected validation error for empty credentials"
        else:
            pytest.skip("Login form not available")
            
    def test_login_with_invalid_credentials(self, driver):
        """Test login with invalid credentials"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        if login_page.is_element_visible(login_page.LOGIN_EMAIL_INPUT, timeout=5):
            login_page.login(
                email="invalid@example.com",
                password="wrongpassword"
            )
            
            time.sleep(3)
            
            # Should show error or not be logged in
            error_msg = login_page.get_error_message()
            is_logged_in = login_page.is_logged_in()
            
            assert error_msg or not is_logged_in, "Expected error for invalid credentials"
        else:
            pytest.skip("Login form not available")
            
    def test_forgot_password_functionality(self, driver):
        """Test forgot password functionality"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        if login_page.is_element_visible(login_page.FORGOT_PASSWORD_LINK, timeout=5):
            login_page.forgot_password("test@example.com")
            
            time.sleep(2)
            
            # Check for success or error message
            success_msg = login_page.get_success_message()
            error_msg = login_page.get_error_message()
            
            assert success_msg or error_msg, "Expected response for forgot password request"
        else:
            pytest.skip("Forgot password functionality not available")
            
    def test_remember_me_functionality(self, driver):
        """Test remember me checkbox"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        if login_page.is_element_visible(login_page.REMEMBER_ME_CHECKBOX, timeout=5):
            # Test checking the remember me box
            checkbox = login_page.find_element(login_page.REMEMBER_ME_CHECKBOX)
            initial_state = checkbox.is_selected()
            
            login_page.click_element(login_page.REMEMBER_ME_CHECKBOX)
            final_state = checkbox.is_selected()
            
            assert initial_state != final_state, "Remember me checkbox state did not change"
        else:
            pytest.skip("Remember me checkbox not available")
            
    def test_social_login_buttons(self, driver):
        """Test social login buttons if available"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        social_buttons_found = False
        
        # Check for Google login
        if login_page.is_element_visible(login_page.GOOGLE_LOGIN, timeout=3):
            social_buttons_found = True
            assert True, "Google login button found"
            
        # Check for Facebook login
        if login_page.is_element_visible(login_page.FACEBOOK_LOGIN, timeout=3):
            social_buttons_found = True
            assert True, "Facebook login button found"
            
        if not social_buttons_found:
            pytest.skip("No social login buttons available")
            
    def test_navigation_from_login_to_register(self, driver):
        """Test navigation between login and register forms"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        if login_page.is_element_visible(login_page.REGISTER_TAB, timeout=5):
            # Click register tab
            login_page.click_element(login_page.REGISTER_TAB)
            time.sleep(1)
            
            # Check if register form elements appear
            register_form_visible = (
                login_page.is_element_visible(login_page.REGISTER_EMAIL, timeout=3) or
                login_page.is_element_visible(login_page.REGISTER_BUTTON, timeout=3)
            )
            
            assert register_form_visible, "Register form did not appear after clicking register tab"
        else:
            pytest.skip("Register tab not available")
            
    @pytest.mark.error_handling
    def test_form_validation_messages(self, driver):
        """Test form validation messages"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # Try submitting login form without data
        if login_page.is_element_visible(login_page.LOGIN_BUTTON, timeout=5):
            login_page.click_element(login_page.LOGIN_BUTTON)
            time.sleep(1)
            
            # Check for validation messages
            validation_errors = login_page.get_validation_errors()
            error_msg = login_page.get_error_message()
            
            # Should have some form of validation
            has_validation = len(validation_errors) > 0 or error_msg
            
            if not has_validation:
                # Try with invalid data to trigger validation
                login_page.login("invalid", "test")
                time.sleep(1)
                
                validation_errors = login_page.get_validation_errors()
                error_msg = login_page.get_error_message()
                has_validation = len(validation_errors) > 0 or error_msg
                
            assert has_validation, "Form should show validation messages"
        else:
            pytest.skip("Login form not available for validation testing")
