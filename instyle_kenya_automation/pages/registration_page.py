"""Registration page object model"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class RegistrationPage(BasePage):
    """Registration page object model for instylekenya.co.ke"""
    
    # Locators
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input[name='first_name'], input[name='firstName'], #first_name, #customer_first_name")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[name='last_name'], input[name='lastName'], #last_name, #customer_last_name")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email'], input[type='email'], #email, #customer_email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password'], input[type='password'], #password, #customer_password")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password_confirmation'], input[name='confirm_password'], #confirm_password")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[name='phone'], input[type='tel'], #phone, #customer_phone")
    
    # Additional fields that might be present
    DATE_OF_BIRTH_INPUT = (By.CSS_SELECTOR, "input[name='dob'], input[name='date_of_birth'], #dob")
    GENDER_SELECT = (By.CSS_SELECTOR, "select[name='gender'], #gender")
    
    # Checkboxes and agreements
    TERMS_CHECKBOX = (By.CSS_SELECTOR, "input[name='terms'], input[name='agree_terms'], #agree_terms")
    NEWSLETTER_CHECKBOX = (By.CSS_SELECTOR, "input[name='newsletter'], input[name='subscribe'], #newsletter")
    PRIVACY_CHECKBOX = (By.CSS_SELECTOR, "input[name='privacy'], input[name='agree_privacy'], #privacy")
    
    # Buttons
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], .btn--primary")
    
    # Links
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login'], a:contains('Login'), a:contains('Sign in')")
    TERMS_LINK = (By.CSS_SELECTOR, "a[href*='terms'], a:contains('Terms')")
    PRIVACY_LINK = (By.CSS_SELECTOR, "a[href*='privacy'], a:contains('Privacy')")
    
    # Messages
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .alert-error, .form__message--error, .errors")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .alert-success, .form__message--success")
    FIELD_ERRORS = (By.CSS_SELECTOR, ".field-error, .input-error, .error-message")
    
    # Form and page elements
    REGISTRATION_FORM = (By.CSS_SELECTOR, "form, .register-form, #create_customer")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1, .page-title, .register-title")
    
    def __init__(self, driver):
        """Initialize registration page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
    def load(self):
        """Load the registration page"""
        self.go_to(Config.URLS["register"])
        return self
    
    def is_loaded(self) -> bool:
        """Check if registration page is loaded
        
        Returns:
            True if page is loaded, False otherwise
        """
        return (self.is_element_visible(self.REGISTRATION_FORM) and 
                (self.is_element_visible(self.EMAIL_INPUT) or 
                 "register" in self.get_current_url().lower()))
    
    def register_user(self, user_data: dict) -> bool:
        """Register a new user
        
        Args:
            user_data: Dictionary containing user information
                Required keys: email, password
                Optional keys: first_name, last_name, phone, confirm_password
                
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            # Fill first name if field exists
            if "first_name" in user_data and self.is_element_present(self.FIRST_NAME_INPUT):
                if not self.send_keys_to_element(self.FIRST_NAME_INPUT, user_data["first_name"]):
                    logger.error("Failed to enter first name")
                    return False
            
            # Fill last name if field exists
            if "last_name" in user_data and self.is_element_present(self.LAST_NAME_INPUT):
                if not self.send_keys_to_element(self.LAST_NAME_INPUT, user_data["last_name"]):
                    logger.error("Failed to enter last name")
                    return False
            
            # Fill email (required)
            if not self.send_keys_to_element(self.EMAIL_INPUT, user_data["email"]):
                logger.error("Failed to enter email")
                return False
            
            # Fill password (required)
            if not self.send_keys_to_element(self.PASSWORD_INPUT, user_data["password"]):
                logger.error("Failed to enter password")
                return False
            
            # Fill confirm password if field exists
            if self.is_element_present(self.CONFIRM_PASSWORD_INPUT):
                confirm_password = user_data.get("confirm_password", user_data["password"])
                if not self.send_keys_to_element(self.CONFIRM_PASSWORD_INPUT, confirm_password):
                    logger.error("Failed to enter confirm password")
                    return False
            
            # Fill phone if provided and field exists
            if "phone" in user_data and self.is_element_present(self.PHONE_INPUT):
                if not self.send_keys_to_element(self.PHONE_INPUT, user_data["phone"]):
                    logger.error("Failed to enter phone number")
                    return False
            
            # Accept terms if checkbox exists
            if self.is_element_present(self.TERMS_CHECKBOX):
                if not self.click_element(self.TERMS_CHECKBOX):
                    logger.error("Failed to accept terms")
                    return False
            
            # Accept privacy if checkbox exists
            if self.is_element_present(self.PRIVACY_CHECKBOX):
                if not self.click_element(self.PRIVACY_CHECKBOX):
                    logger.error("Failed to accept privacy policy")
                    return False
            
            # Subscribe to newsletter if requested
            if user_data.get("subscribe_newsletter", False) and self.is_element_present(self.NEWSLETTER_CHECKBOX):
                self.click_element(self.NEWSLETTER_CHECKBOX)
            
            # Click register button
            if not self.click_element(self.REGISTER_BUTTON):
                logger.error("Failed to click register button")
                return False
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Check if registration was successful
            if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5):
                logger.info("Registration successful")
                return True
            
            # Check if redirected away from registration page (another success indicator)
            if "register" not in self.get_current_url().lower():
                logger.info("Registration successful - redirected")
                return True
            
            # Check for error messages
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
                error_text = self.get_element_text(self.ERROR_MESSAGE)
                logger.error(f"Registration failed with error: {error_text}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Registration failed with exception: {str(e)}")
            return False
    
    def get_error_message(self) -> str:
        """Get general error message if present
        
        Returns:
            Error message text or empty string
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
                return self.get_element_text(self.ERROR_MESSAGE)
            return ""
        except Exception:
            return ""
    
    def get_field_errors(self) -> list:
        """Get all field-specific error messages
        
        Returns:
            List of field error messages
        """
        try:
            error_elements = self.find_elements(self.FIELD_ERRORS)
            return [error.text for error in error_elements if error.text.strip()]
        except Exception:
            return []
    
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
    
    def click_login_link(self) -> bool:
        """Click on login link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.LOGIN_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def click_terms_link(self) -> bool:
        """Click on terms and conditions link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        return self.click_element(self.TERMS_LINK)
    
    def click_privacy_link(self) -> bool:
        """Click on privacy policy link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        return self.click_element(self.PRIVACY_LINK)
    
    def is_terms_checkbox_checked(self) -> bool:
        """Check if terms checkbox is checked
        
        Returns:
            True if checked, False otherwise
        """
        try:
            if self.is_element_present(self.TERMS_CHECKBOX):
                element = self.find_element(self.TERMS_CHECKBOX)
                return element.is_selected()
            return True  # If no checkbox, assume terms are accepted
        except Exception:
            return False
    
    def is_newsletter_checkbox_checked(self) -> bool:
        """Check if newsletter checkbox is checked
        
        Returns:
            True if checked, False otherwise
        """
        try:
            if self.is_element_present(self.NEWSLETTER_CHECKBOX):
                element = self.find_element(self.NEWSLETTER_CHECKBOX)
                return element.is_selected()
            return False
        except Exception:
            return False
    
    def clear_form(self) -> None:
        """Clear all form fields"""
        try:
            fields = [
                self.FIRST_NAME_INPUT,
                self.LAST_NAME_INPUT,
                self.EMAIL_INPUT,
                self.PASSWORD_INPUT,
                self.CONFIRM_PASSWORD_INPUT,
                self.PHONE_INPUT
            ]
            
            for field_locator in fields:
                if self.is_element_present(field_locator):
                    field = self.find_element(field_locator)
                    field.clear()
                    
        except Exception as e:
            logger.error(f"Failed to clear form: {str(e)}")
    
    def get_page_title_text(self) -> str:
        """Get the page title text
        
        Returns:
            Page title text
        """
        return self.get_element_text(self.PAGE_TITLE)
    
    def is_form_valid(self) -> bool:
        """Check if the form appears to be valid/complete
        
        Returns:
            True if form has required elements, False otherwise
        """
        return (self.is_element_present(self.EMAIL_INPUT) and 
                self.is_element_present(self.PASSWORD_INPUT) and 
                self.is_element_present(self.REGISTER_BUTTON))
