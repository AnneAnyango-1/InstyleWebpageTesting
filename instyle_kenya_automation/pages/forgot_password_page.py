"""Forgot password page object model"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class ForgotPasswordPage(BasePage):
    """Forgot password page object model for instylekenya.co.ke"""
    
    # Form elements
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email'], input[type='email'], #email, #customer_email")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], .btn--primary")
    
    # Page elements
    PAGE_TITLE = (By.CSS_SELECTOR, "h1, .page-title, .forgot-password-title")
    INSTRUCTIONS = (By.CSS_SELECTOR, ".instructions, .forgot-password-text, .form-description")
    FORM = (By.CSS_SELECTOR, "form, .forgot-password-form")
    
    # Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .alert-success, .form__message--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .alert-error, .form__message--error")
    
    # Links
    BACK_TO_LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login'], a:contains('Login'), a:contains('Sign in')")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href*='register'], a:contains('Register'), a:contains('Sign up')")
    
    def __init__(self, driver):
        """Initialize forgot password page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
    def is_loaded(self) -> bool:
        """Check if forgot password page is loaded
        
        Returns:
            True if page is loaded, False otherwise
        """
        return ("forgot" in self.get_current_url().lower() or 
                "recover" in self.get_current_url().lower() or
                self.is_element_visible(self.EMAIL_INPUT))
    
    def reset_password(self, email: str) -> bool:
        """Submit password reset request
        
        Args:
            email: Email address to send reset link to
            
        Returns:
            True if reset request was submitted successfully, False otherwise
        """
        try:
            # Enter email address
            if not self.send_keys_to_element(self.EMAIL_INPUT, email):
                logger.error("Failed to enter email")
                return False
            
            # Click submit button
            if not self.click_element(self.SUBMIT_BUTTON):
                logger.error("Failed to click submit button")
                return False
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Check for success message
            if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5):
                logger.info("Password reset request submitted successfully")
                return True
            
            # Check for error message
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
                error_text = self.get_element_text(self.ERROR_MESSAGE)
                logger.error(f"Password reset failed with error: {error_text}")
                return False
            
            # If no explicit message, assume success
            return True
            
        except Exception as e:
            logger.error(f"Password reset failed with exception: {str(e)}")
            return False
    
    def get_page_title_text(self) -> str:
        """Get the page title text
        
        Returns:
            Page title text
        """
        return self.get_element_text(self.PAGE_TITLE)
    
    def get_instructions_text(self) -> str:
        """Get the instructions text
        
        Returns:
            Instructions text
        """
        return self.get_element_text(self.INSTRUCTIONS)
    
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
    
    def click_back_to_login(self) -> bool:
        """Click back to login link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.BACK_TO_LOGIN_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def click_register_link(self) -> bool:
        """Click register link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.REGISTER_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def clear_email_field(self) -> None:
        """Clear the email input field"""
        try:
            email_field = self.find_element(self.EMAIL_INPUT)
            email_field.clear()
        except Exception as e:
            logger.error(f"Failed to clear email field: {str(e)}")
    
    def is_form_valid(self) -> bool:
        """Check if the form appears to be valid/complete
        
        Returns:
            True if form has required elements, False otherwise
        """
        return (self.is_element_present(self.EMAIL_INPUT) and 
                self.is_element_present(self.SUBMIT_BUTTON))
