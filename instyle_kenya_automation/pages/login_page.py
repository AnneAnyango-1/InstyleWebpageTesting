"""Login page object model"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Login page object model for instylekenya.co.ke"""
    
    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email'], input[type='email'], #email, #customer_email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password'], input[type='password'], #password, #customer_password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], .btn--primary")
    
    # Remember me checkbox
    REMEMBER_ME_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox'], #remember_me")
    
    # Links
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href*='forgot'], a[href*='recover'], a:contains('Forgot')")
    CREATE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href*='register'], a[href*='signup'], a:contains('Create'), a:contains('Sign up')")
    
    # Error and success messages
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .alert-error, .form__message--error, .errors")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .alert-success, .form__message--success")
    
    # Page elements
    LOGIN_FORM = (By.CSS_SELECTOR, "form, .login-form, #customer_login")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1, .page-title, .login-title")
    
    def __init__(self, driver):
        """Initialize login page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
    def load(self):
        """Load the login page"""
        self.go_to(Config.URLS["login"])
        return self
    
    def is_loaded(self) -> bool:
        """Check if login page is loaded
        
        Returns:
            True if page is loaded, False otherwise
        """
        return (self.is_element_visible(self.LOGIN_FORM) and 
                (self.is_element_visible(self.EMAIL_INPUT) or 
                 "login" in self.get_current_url().lower()))
    
    def login(self, email: str, password: str, remember_me: bool = False) -> bool:
        """Perform login operation
        
        Args:
            email: User email
            password: User password
            remember_me: Whether to check remember me option
            
        Returns:
            True if login was successful, False otherwise
        """
        try:
            # Enter email
            if not self.send_keys_to_element(self.EMAIL_INPUT, email):
                logger.error("Failed to enter email")
                return False
            
            # Enter password
            if not self.send_keys_to_element(self.PASSWORD_INPUT, password):
                logger.error("Failed to enter password")
                return False
            
            # Check remember me if requested
            if remember_me and self.is_element_present(self.REMEMBER_ME_CHECKBOX):
                self.click_element(self.REMEMBER_ME_CHECKBOX)
            
            # Click login button
            if not self.click_element(self.LOGIN_BUTTON):
                logger.error("Failed to click login button")
                return False
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Check if login was successful (redirected away from login page)
            if "login" not in self.get_current_url().lower():
                logger.info("Login successful")
                return True
            
            # Check for error messages
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
                error_text = self.get_element_text(self.ERROR_MESSAGE)
                logger.error(f"Login failed with error: {error_text}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Login failed with exception: {str(e)}")
            return False
    
    def get_error_message(self) -> str:
        """Get error message if present
        
        Returns:
            Error message text or empty string
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
                return self.get_element_text(self.ERROR_MESSAGE)
            return ""
        except Exception:
            return ""
    
    def get_success_message(self) -> str:
        """Get success message if present
        
        Returns:
            Success message text or empty string
        """
        try:
            if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=3):
                return self.get_element_text(self.SUCCESS_MESSAGE)
            return ""
        except Exception:
            return ""
    
    def click_forgot_password(self) -> bool:
        """Click on forgot password link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.FORGOT_PASSWORD_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def click_create_account(self) -> bool:
        """Click on create account/register link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.CREATE_ACCOUNT_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def is_remember_me_checked(self) -> bool:
        """Check if remember me checkbox is checked
        
        Returns:
            True if checked, False otherwise
        """
        try:
            element = self.find_element(self.REMEMBER_ME_CHECKBOX)
            return element.is_selected()
        except Exception:
            return False
    
    def get_page_title_text(self) -> str:
        """Get the page title text
        
        Returns:
            Page title text
        """
        return self.get_element_text(self.PAGE_TITLE)
    
    def clear_form(self) -> None:
        """Clear the login form"""
        try:
            email_field = self.find_element(self.EMAIL_INPUT)
            password_field = self.find_element(self.PASSWORD_INPUT)
            
            email_field.clear()
            password_field.clear()
        except Exception as e:
            logger.error(f"Failed to clear form: {str(e)}")
    
    def is_form_valid(self) -> bool:
        """Check if the form appears to be valid/complete
        
        Returns:
            True if form has required elements, False otherwise
        """
        return (self.is_element_present(self.EMAIL_INPUT) and 
                self.is_element_present(self.PASSWORD_INPUT) and 
                self.is_element_present(self.LOGIN_BUTTON))
