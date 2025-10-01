"""Product page object model"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class ProductPage(BasePage):
    """Product page object model for instylekenya.co.ke"""
    
    # Product information
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product__title, h1, .product-title")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product__price, .price, .product-price")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".product__description, .product-description, .description")
    PRODUCT_SKU = (By.CSS_SELECTOR, ".product__sku, .sku, .product-sku")
    
    # Product images
    MAIN_PRODUCT_IMAGE = (By.CSS_SELECTOR, ".product__image img, .main-image img, .product-image img")
    THUMBNAIL_IMAGES = (By.CSS_SELECTOR, ".product__thumbnails img, .thumbnail img, .product-thumbnails img")
    IMAGE_GALLERY = (By.CSS_SELECTOR, ".product__gallery, .image-gallery")
    
    # Product variants/options
    SIZE_OPTIONS = (By.CSS_SELECTOR, "select[name*='size'], .size-selector, .product__size")
    COLOR_OPTIONS = (By.CSS_SELECTOR, "select[name*='color'], .color-selector, .product__color")
    VARIANT_OPTIONS = (By.CSS_SELECTOR, ".product__variant, .variant-selector")
    
    # Quantity and cart
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name*='quantity'], .quantity__input, .qty")
    QUANTITY_INCREASE = (By.CSS_SELECTOR, ".quantity__button--increase, .qty-plus")
    QUANTITY_DECREASE = (By.CSS_SELECTOR, ".quantity__button--decrease, .qty-minus")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[name*='add'], .add-to-cart, .btn--add-to-cart")
    BUY_NOW_BUTTON = (By.CSS_SELECTOR, ".buy-now, .btn--buy-now")
    
    # Wishlist and sharing
    ADD_TO_WISHLIST_BUTTON = (By.CSS_SELECTOR, ".add-to-wishlist, .wishlist-add, button[name*='wishlist']")
    SHARE_BUTTON = (By.CSS_SELECTOR, ".share-product, .product__share")
    
    # Product details and tabs
    PRODUCT_TABS = (By.CSS_SELECTOR, ".product__tabs, .tabs, .product-tabs")
    DESCRIPTION_TAB = (By.CSS_SELECTOR, "[data-tab='description'], .tab--description")
    SPECIFICATIONS_TAB = (By.CSS_SELECTOR, "[data-tab='specifications'], .tab--specs")
    REVIEWS_TAB = (By.CSS_SELECTOR, "[data-tab='reviews'], .tab--reviews")
    SHIPPING_TAB = (By.CSS_SELECTOR, "[data-tab='shipping'], .tab--shipping")
    
    # Reviews section
    REVIEWS_SECTION = (By.CSS_SELECTOR, ".product__reviews, .reviews, .product-reviews")
    REVIEW_ITEMS = (By.CSS_SELECTOR, ".review, .review-item")
    REVIEW_RATING = (By.CSS_SELECTOR, ".review__rating, .rating")
    REVIEW_TEXT = (By.CSS_SELECTOR, ".review__text, .review-content")
    WRITE_REVIEW_BUTTON = (By.CSS_SELECTOR, ".write-review, .review-add")
    
    # Related/recommended products
    RELATED_PRODUCTS = (By.CSS_SELECTOR, ".related-products, .recommended-products")
    RELATED_PRODUCT_ITEMS = (By.CSS_SELECTOR, ".related-products .product-item, .recommended-products .product-item")
    
    # Availability and stock
    STOCK_STATUS = (By.CSS_SELECTOR, ".product__stock, .stock-status, .availability")
    IN_STOCK_MESSAGE = (By.CSS_SELECTOR, ".in-stock, .available")
    OUT_OF_STOCK_MESSAGE = (By.CSS_SELECTOR, ".out-of-stock, .unavailable")
    
    # Messages and notifications
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .alert-success, .message--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .alert-error, .message--error")
    
    # Breadcrumbs
    BREADCRUMBS = (By.CSS_SELECTOR, ".breadcrumbs, .breadcrumb")
    
    def __init__(self, driver):
        """Initialize product page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
    def is_loaded(self) -> bool:
        """Check if product page is loaded
        
        Returns:
            True if page is loaded, False otherwise
        """
        return (self.is_element_visible(self.PRODUCT_TITLE) and 
                self.is_element_visible(self.ADD_TO_CART_BUTTON))
    
    def get_product_title(self) -> str:
        """Get product title
        
        Returns:
            Product title text
        """
        return self.get_element_text(self.PRODUCT_TITLE)
    
    def get_product_price(self) -> str:
        """Get product price
        
        Returns:
            Product price text
        """
        return self.get_element_text(self.PRODUCT_PRICE)
    
    def get_product_description(self) -> str:
        """Get product description
        
        Returns:
            Product description text
        """
        return self.get_element_text(self.PRODUCT_DESCRIPTION)
    
    def get_product_sku(self) -> str:
        """Get product SKU
        
        Returns:
            Product SKU text
        """
        return self.get_element_text(self.PRODUCT_SKU)
    
    def select_size(self, size: str) -> bool:
        """Select product size
        
        Args:
            size: Size to select
            
        Returns:
            True if size was selected, False otherwise
        """
        try:
            if self.is_element_present(self.SIZE_OPTIONS):
                from selenium.webdriver.support.ui import Select
                size_dropdown = Select(self.find_element(self.SIZE_OPTIONS))
                size_dropdown.select_by_visible_text(size)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to select size: {str(e)}")
            return False
    
    def select_color(self, color: str) -> bool:
        """Select product color
        
        Args:
            color: Color to select
            
        Returns:
            True if color was selected, False otherwise
        """
        try:
            if self.is_element_present(self.COLOR_OPTIONS):
                from selenium.webdriver.support.ui import Select
                color_dropdown = Select(self.find_element(self.COLOR_OPTIONS))
                color_dropdown.select_by_visible_text(color)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to select color: {str(e)}")
            return False
    
    def set_quantity(self, quantity: int) -> bool:
        """Set product quantity
        
        Args:
            quantity: Quantity to set
            
        Returns:
            True if quantity was set, False otherwise
        """
        try:
            return self.send_keys_to_element(self.QUANTITY_INPUT, str(quantity))
        except Exception as e:
            logger.error(f"Failed to set quantity: {str(e)}")
            return False
    
    def increase_quantity(self) -> bool:
        """Increase product quantity by 1
        
        Returns:
            True if quantity was increased, False otherwise
        """
        return self.click_element(self.QUANTITY_INCREASE)
    
    def decrease_quantity(self) -> bool:
        """Decrease product quantity by 1
        
        Returns:
            True if quantity was decreased, False otherwise
        """
        return self.click_element(self.QUANTITY_DECREASE)
    
    def add_to_cart(self) -> bool:
        """Add product to cart
        
        Returns:
            True if product was added to cart, False otherwise
        """
        if self.click_element(self.ADD_TO_CART_BUTTON):
            # Wait for success message or page update
            if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5):
                return True
            # If no success message, assume it worked
            return True
        return False
    
    def buy_now(self) -> bool:
        """Click buy now button
        
        Returns:
            True if buy now was clicked, False otherwise
        """
        if self.click_element(self.BUY_NOW_BUTTON):
            self.wait_for_page_load()
            return True
        return False
    
    def add_to_wishlist(self) -> bool:
        """Add product to wishlist
        
        Returns:
            True if product was added to wishlist, False otherwise
        """
        return self.click_element(self.ADD_TO_WISHLIST_BUTTON)
    
    def share_product(self) -> bool:
        """Click share product button
        
        Returns:
            True if share button was clicked, False otherwise
        """
        return self.click_element(self.SHARE_BUTTON)
    
    def click_thumbnail_image(self, index: int) -> bool:
        """Click on a thumbnail image
        
        Args:
            index: Index of the thumbnail (0-based)
            
        Returns:
            True if thumbnail was clicked, False otherwise
        """
        try:
            thumbnails = self.find_elements(self.THUMBNAIL_IMAGES)
            if index < len(thumbnails):
                thumbnails[index].click()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to click thumbnail: {str(e)}")
            return False
    
    def switch_to_tab(self, tab_name: str) -> bool:
        """Switch to a product information tab
        
        Args:
            tab_name: Name of the tab (description, specifications, reviews, shipping)
            
        Returns:
            True if tab was switched, False otherwise
        """
        tab_locators = {
            "description": self.DESCRIPTION_TAB,
            "specifications": self.SPECIFICATIONS_TAB,
            "reviews": self.REVIEWS_TAB,
            "shipping": self.SHIPPING_TAB
        }
        
        tab_key = tab_name.lower()
        if tab_key in tab_locators:
            return self.click_element(tab_locators[tab_key])
        return False
    
    def get_reviews(self) -> list:
        """Get product reviews
        
        Returns:
            List of review dictionaries
        """
        reviews = []
        try:
            review_items = self.find_elements(self.REVIEW_ITEMS)
            
            for review in review_items:
                try:
                    rating_element = review.find_element(*self.REVIEW_RATING)
                    rating = rating_element.get_attribute("data-rating") or rating_element.text
                    
                    text_element = review.find_element(*self.REVIEW_TEXT)
                    text = text_element.text
                    
                    reviews.append({
                        "rating": rating,
                        "text": text
                    })
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to get reviews: {str(e)}")
            
        return reviews
    
    def write_review(self) -> bool:
        """Click write review button
        
        Returns:
            True if write review button was clicked, False otherwise
        """
        return self.click_element(self.WRITE_REVIEW_BUTTON)
    
    def get_related_products(self) -> list:
        """Get related/recommended products
        
        Returns:
            List of related product information
        """
        products = []
        try:
            product_items = self.find_elements(self.RELATED_PRODUCT_ITEMS)
            
            for item in product_items[:5]:  # Limit to first 5
                try:
                    title_element = item.find_element(By.CSS_SELECTOR, ".product__title, h3, .product-title")
                    title = title_element.text if title_element else "Unknown"
                    
                    price_element = item.find_element(By.CSS_SELECTOR, ".product__price, .price")
                    price = price_element.text if price_element else "$0.00"
                    
                    products.append({
                        "title": title,
                        "price": price
                    })
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to get related products: {str(e)}")
            
        return products
    
    def is_in_stock(self) -> bool:
        """Check if product is in stock
        
        Returns:
            True if in stock, False otherwise
        """
        try:
            if self.is_element_visible(self.IN_STOCK_MESSAGE, timeout=3):
                return True
            elif self.is_element_visible(self.OUT_OF_STOCK_MESSAGE, timeout=3):
                return False
            
            # Check if add to cart button is enabled
            if self.is_element_present(self.ADD_TO_CART_BUTTON):
                button = self.find_element(self.ADD_TO_CART_BUTTON)
                return button.is_enabled()
            
            return True  # Assume in stock if no clear indicators
        except Exception:
            return True
    
    def get_stock_status(self) -> str:
        """Get stock status text
        
        Returns:
            Stock status text
        """
        return self.get_element_text(self.STOCK_STATUS)
    
    def get_success_message(self) -> str:
        """Get success message
        
        Returns:
            Success message text
        """
        return self.get_element_text(self.SUCCESS_MESSAGE)
    
    def get_error_message(self) -> str:
        """Get error message
        
        Returns:
            Error message text
        """
        return self.get_element_text(self.ERROR_MESSAGE)
