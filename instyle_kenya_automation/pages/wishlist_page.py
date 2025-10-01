"""Wishlist page object model"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class WishlistPage(BasePage):
    """Wishlist page object model for instylekenya.co.ke"""
    
    # Locators
    WISHLIST_ITEMS = (By.CSS_SELECTOR, ".wishlist__item, .wishlist-item, .grid__item")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".wishlist__item-title, .product__title, h3")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".wishlist__item-price, .product__price, .price")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".wishlist__item-image img, .product__image img")
    PRODUCT_LINKS = (By.CSS_SELECTOR, ".wishlist__item-link, .product__link, a")
    
    # Action buttons
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".add-to-cart, button[name*='add'], .btn--add-to-cart")
    REMOVE_FROM_WISHLIST_BUTTONS = (By.CSS_SELECTOR, ".remove-wishlist, .wishlist__remove, button[name*='remove']")
    MOVE_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".move-to-cart, .wishlist__move")
    
    # Empty wishlist
    EMPTY_WISHLIST_MESSAGE = (By.CSS_SELECTOR, ".wishlist--empty, .empty-wishlist, .wishlist__empty")
    CONTINUE_SHOPPING_LINK = (By.CSS_SELECTOR, ".continue-shopping, .wishlist__continue")
    
    # Wishlist management
    SHARE_WISHLIST_BUTTON = (By.CSS_SELECTOR, ".share-wishlist, .wishlist__share")
    CLEAR_WISHLIST_BUTTON = (By.CSS_SELECTOR, ".clear-wishlist, .wishlist__clear")
    WISHLIST_COUNT = (By.CSS_SELECTOR, ".wishlist-count, .wishlist__count")
    
    # Sorting and filtering
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[name*='sort'], .sort-dropdown")
    FILTER_OPTIONS = (By.CSS_SELECTOR, ".filter-option, .wishlist__filter")
    
    # Page elements
    PAGE_TITLE = (By.CSS_SELECTOR, "h1, .page-title, .wishlist-title")
    WISHLIST_FORM = (By.CSS_SELECTOR, "form, .wishlist-form")
    
    def __init__(self, driver):
        """Initialize wishlist page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
    def load(self):
        """Load the wishlist page"""
        self.go_to(Config.URLS["wishlist"])
        return self
    
    def is_loaded(self) -> bool:
        """Check if wishlist page is loaded
        
        Returns:
            True if page is loaded, False otherwise
        """
        return ("wishlist" in self.get_current_url().lower() or 
                self.is_element_present(self.WISHLIST_ITEMS) or 
                self.is_element_present(self.EMPTY_WISHLIST_MESSAGE))
    
    def is_wishlist_empty(self) -> bool:
        """Check if wishlist is empty
        
        Returns:
            True if wishlist is empty, False otherwise
        """
        return (self.is_element_visible(self.EMPTY_WISHLIST_MESSAGE) or 
                len(self.find_elements(self.WISHLIST_ITEMS)) == 0)
    
    def get_wishlist_items(self) -> list:
        """Get all items in the wishlist
        
        Returns:
            List of wishlist item dictionaries
        """
        items = []
        try:
            wishlist_items = self.find_elements(self.WISHLIST_ITEMS)
            
            for item in wishlist_items:
                try:
                    # Get product name
                    name_element = item.find_element(*self.PRODUCT_NAMES)
                    name = name_element.text if name_element else "Unknown Product"
                    
                    # Get product price
                    price_element = item.find_element(*self.PRODUCT_PRICES)
                    price = price_element.text if price_element else "$0.00"
                    
                    # Get product link
                    link_element = item.find_element(*self.PRODUCT_LINKS)
                    link = link_element.get_attribute("href") if link_element else ""
                    
                    # Get image src
                    image_element = item.find_element(*self.PRODUCT_IMAGES)
                    image_src = image_element.get_attribute("src") if image_element else ""
                    
                    items.append({
                        "name": name,
                        "price": price,
                        "link": link,
                        "image_src": image_src
                    })
                    
                except Exception as e:
                    logger.warning(f"Could not extract wishlist item info: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to get wishlist items: {str(e)}")
            
        return items
    
    def get_wishlist_item_count(self) -> int:
        """Get the number of items in wishlist
        
        Returns:
            Number of wishlist items
        """
        try:
            return len(self.find_elements(self.WISHLIST_ITEMS))
        except Exception:
            return 0
    
    def add_item_to_cart(self, item_index: int) -> bool:
        """Add a wishlist item to cart
        
        Args:
            item_index: Index of the item to add (0-based)
            
        Returns:
            True if item was added to cart, False otherwise
        """
        try:
            add_to_cart_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
            
            if item_index < len(add_to_cart_buttons):
                add_to_cart_buttons[item_index].click()
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to add item to cart: {str(e)}")
            return False
    
    def remove_item_from_wishlist(self, item_index: int) -> bool:
        """Remove an item from wishlist
        
        Args:
            item_index: Index of the item to remove (0-based)
            
        Returns:
            True if item was removed, False otherwise
        """
        try:
            remove_buttons = self.find_elements(self.REMOVE_FROM_WISHLIST_BUTTONS)
            
            if item_index < len(remove_buttons):
                remove_buttons[item_index].click()
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to remove item from wishlist: {str(e)}")
            return False
    
    def move_item_to_cart(self, item_index: int) -> bool:
        """Move a wishlist item to cart (remove from wishlist and add to cart)
        
        Args:
            item_index: Index of the item to move (0-based)
            
        Returns:
            True if item was moved, False otherwise
        """
        try:
            move_buttons = self.find_elements(self.MOVE_TO_CART_BUTTONS)
            
            if item_index < len(move_buttons):
                move_buttons[item_index].click()
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to move item to cart: {str(e)}")
            return False
    
    def click_product(self, item_index: int) -> bool:
        """Click on a product to view its details
        
        Args:
            item_index: Index of the product to click (0-based)
            
        Returns:
            True if product was clicked, False otherwise
        """
        try:
            wishlist_items = self.find_elements(self.WISHLIST_ITEMS)
            
            if item_index < len(wishlist_items):
                # Try to find product link within the item
                item = wishlist_items[item_index]
                product_link = item.find_element(*self.PRODUCT_LINKS)
                product_link.click()
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to click product: {str(e)}")
            return False
    
    def clear_wishlist(self) -> bool:
        """Clear all items from wishlist
        
        Returns:
            True if wishlist was cleared, False otherwise
        """
        try:
            if self.is_element_present(self.CLEAR_WISHLIST_BUTTON):
                if self.click_element(self.CLEAR_WISHLIST_BUTTON):
                    # Handle confirmation dialog if present
                    try:
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except:
                        pass  # No alert present
                    
                    self.wait_for_page_load()
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to clear wishlist: {str(e)}")
            return False
    
    def share_wishlist(self) -> bool:
        """Click share wishlist button
        
        Returns:
            True if share button was clicked, False otherwise
        """
        try:
            return self.click_element(self.SHARE_WISHLIST_BUTTON)
        except Exception as e:
            logger.error(f"Failed to share wishlist: {str(e)}")
            return False
    
    def continue_shopping(self) -> bool:
        """Click continue shopping link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.CONTINUE_SHOPPING_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def sort_wishlist(self, sort_option: str) -> bool:
        """Sort wishlist items
        
        Args:
            sort_option: Sort option text (e.g., "Price: Low to High")
            
        Returns:
            True if sorting was applied, False otherwise
        """
        try:
            if self.is_element_present(self.SORT_DROPDOWN):
                from selenium.webdriver.support.ui import Select
                sort_dropdown = Select(self.find_element(self.SORT_DROPDOWN))
                sort_dropdown.select_by_visible_text(sort_option)
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to sort wishlist: {str(e)}")
            return False
    
    def get_empty_wishlist_message(self) -> str:
        """Get empty wishlist message
        
        Returns:
            Empty wishlist message text
        """
        return self.get_element_text(self.EMPTY_WISHLIST_MESSAGE)
    
    def get_page_title_text(self) -> str:
        """Get the page title text
        
        Returns:
            Page title text
        """
        return self.get_element_text(self.PAGE_TITLE)
    
    def get_wishlist_count_display(self) -> str:
        """Get wishlist count from display
        
        Returns:
            Wishlist count as displayed on page
        """
        return self.get_element_text(self.WISHLIST_COUNT)
    
    def add_all_to_cart(self) -> bool:
        """Add all wishlist items to cart
        
        Returns:
            True if all items were added, False otherwise
        """
        try:
            item_count = self.get_wishlist_item_count()
            success_count = 0
            
            for i in range(item_count):
                if self.add_item_to_cart(0):  # Always use index 0 as items are removed
                    success_count += 1
            
            return success_count == item_count
            
        except Exception as e:
            logger.error(f"Failed to add all items to cart: {str(e)}")
            return False
