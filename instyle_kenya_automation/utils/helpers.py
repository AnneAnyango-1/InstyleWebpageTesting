"""Common helper functions for tests"""

import time
import logging
from typing import List, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class TestHelpers:
    """Helper functions for test automation"""
    
    @staticmethod
    def wait_for_page_load(driver: WebDriver, timeout: int = 30) -> bool:
        """Wait for page to completely load
        
        Args:
            driver: WebDriver instance
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if page loaded successfully, False otherwise
        """
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            logger.warning(f"Page did not load completely within {timeout} seconds")
            return False
    
    @staticmethod
    def scroll_to_element(driver: WebDriver, element) -> None:
        """Scroll to make element visible
        
        Args:
            driver: WebDriver instance
            element: WebElement to scroll to
        """
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Small delay for smooth scrolling
    
    @staticmethod
    def take_screenshot(driver: WebDriver, filename: str) -> str:
        """Take screenshot and save to file
        
        Args:
            driver: WebDriver instance
            filename: Name of the screenshot file
            
        Returns:
            Path to the saved screenshot
        """
        screenshot_path = f"screenshots/{filename}"
        try:
            driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return ""
    
    @staticmethod
    def get_all_links(driver: WebDriver) -> List[str]:
        """Get all links from the current page
        
        Args:
            driver: WebDriver instance
            
        Returns:
            List of URLs found on the page
        """
        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            return [link.get_attribute("href") for link in links if link.get_attribute("href")]
        except Exception as e:
            logger.error(f"Failed to get links: {str(e)}")
            return []
    
    @staticmethod
    def verify_links_are_working(driver: WebDriver, links: List[str], max_links: int = 10) -> dict:
        """Verify that links are working (basic check)
        
        Args:
            driver: WebDriver instance
            links: List of URLs to check
            max_links: Maximum number of links to check
            
        Returns:
            Dictionary with results
        """
        results = {"working": [], "broken": [], "errors": []}
        
        for i, link in enumerate(links[:max_links]):
            try:
                original_url = driver.current_url
                driver.get(link)
                
                # Check if page loaded successfully
                if "404" not in driver.title.lower() and "error" not in driver.title.lower():
                    results["working"].append(link)
                else:
                    results["broken"].append(link)
                
                # Go back to original page
                driver.get(original_url)
                
            except Exception as e:
                results["errors"].append({"link": link, "error": str(e)})
                logger.error(f"Error checking link {link}: {str(e)}")
        
        return results
    
    @staticmethod
    def wait_and_click(driver: WebDriver, locator: tuple, timeout: int = 10) -> bool:
        """Wait for element to be clickable and click it
        
        Args:
            driver: WebDriver instance
            locator: Tuple of (By, value)
            timeout: Maximum time to wait
            
        Returns:
            True if clicked successfully, False otherwise
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except TimeoutException:
            logger.error(f"Element not clickable within {timeout} seconds: {locator}")
            return False
    
    @staticmethod
    def safe_send_keys(driver: WebDriver, locator: tuple, text: str, timeout: int = 10) -> bool:
        """Safely send keys to an element
        
        Args:
            driver: WebDriver instance
            locator: Tuple of (By, value)
            text: Text to send
            timeout: Maximum time to wait
            
        Returns:
            True if successful, False otherwise
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            logger.error(f"Element not found or not clickable within {timeout} seconds: {locator}")
            return False
