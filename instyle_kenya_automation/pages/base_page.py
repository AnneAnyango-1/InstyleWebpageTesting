"""Base page class containing common methods for all page objects"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config
import logging
import time

logger = logging.getLogger(__name__)

class BasePage:
    """Base page class with common functionality for all pages"""
    
    def __init__(self, driver: WebDriver):
        """Initialize the base page
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
    
    def go_to(self, url: str) -> None:
        """Navigate to a specific URL
        
        Args:
            url: URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: int = 30) -> bool:
        """Wait for page to load completely
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if page loaded, False otherwise
        """
        try:
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            logger.warning(f"Page did not load within {timeout} seconds")
            return False
    
    def find_element(self, locator: tuple, timeout: int = None) -> object:
        """Find an element with explicit wait
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum time to wait
            
        Returns:
            WebElement if found
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
        
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator: tuple, timeout: int = None) -> list:
        """Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum time to wait
            
        Returns:
            List of WebElements
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            logger.warning(f"Elements not found: {locator}")
            return []
    
    def is_element_present(self, locator: tuple) -> bool:
        """Check if element is present on the page
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            True if element is present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """Check if element is visible on the page
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum time to wait
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def click_element(self, locator: tuple, timeout: int = None) -> bool:
        """Click an element with explicit wait
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum time to wait
            
        Returns:
            True if clicked successfully, False otherwise
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except TimeoutException:
            logger.error(f"Element not clickable: {locator}")
            return False
    
    def send_keys_to_element(self, locator: tuple, text: str, clear: bool = True, timeout: int = None) -> bool:
        """Send keys to an element
        
        Args:
            locator: Tuple of (By, value)
            text: Text to send
            clear: Whether to clear the field first
            timeout: Maximum time to wait
            
        Returns:
            True if successful, False otherwise
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            if clear:
                element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            logger.error(f"Could not send keys to element: {locator}")
            return False
    
    def get_element_text(self, locator: tuple, timeout: int = None) -> str:
        """Get text from an element
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum time to wait
            
        Returns:
            Element text or empty string if not found
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.text
        except TimeoutException:
            logger.error(f"Could not get text from element: {locator}")
            return ""
    
    def get_element_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> str:
        """Get attribute value from an element
        
        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name
            timeout: Maximum time to wait
            
        Returns:
            Attribute value or empty string if not found
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.get_attribute(attribute) or ""
        except TimeoutException:
            logger.error(f"Could not get attribute {attribute} from element: {locator}")
            return ""
    
    def scroll_to_element(self, locator: tuple) -> None:
        """Scroll to make element visible
        
        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Small delay for smooth scrolling
        except Exception as e:
            logger.error(f"Could not scroll to element {locator}: {str(e)}")
    
    def hover_over_element(self, locator: tuple) -> bool:
        """Hover over an element
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
            return True
        except Exception as e:
            logger.error(f"Could not hover over element {locator}: {str(e)}")
            return False
    
    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = 10) -> bool:
        """Wait for an element to disappear from the page
        
        Args:
            locator: Tuple of (By, value)
            timeout: Maximum time to wait
            
        Returns:
            True if element disappeared, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def get_page_title(self) -> str:
        """Get the current page title
        
        Returns:
            Page title
        """
        return self.driver.title
    
    def get_current_url(self) -> str:
        """Get the current URL
        
        Returns:
            Current URL
        """
        return self.driver.current_url
    
    def refresh_page(self) -> None:
        """Refresh the current page"""
        self.driver.refresh()
        self.wait_for_page_load()
    
    def go_back(self) -> None:
        """Navigate back in browser history"""
        self.driver.back()
        self.wait_for_page_load()
    
    def take_screenshot(self, filename: str) -> str:
        """Take a screenshot of the current page
        
        Args:
            filename: Name for the screenshot file
            
        Returns:
            Path to the screenshot file
        """
        screenshot_path = f"screenshots/{filename}"
        try:
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return ""
