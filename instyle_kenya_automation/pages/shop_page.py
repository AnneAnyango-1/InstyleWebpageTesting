from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class ShopPage(BasePage):
    """Page Object Model for Shop/Product Listing Page"""
    
    # Page header and info
    PRODUCTS_COUNT = (By.XPATH, "//*[contains(text(), 'Products found')] | //*[contains(text(), 'products')]")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1, .page-title, [class*='title']")
    
    # Product grid and listings
    PRODUCT_GRID = (By.CSS_SELECTOR, ".products-grid, .product-list, [class*='product-grid']")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card, .product-item, [class*='product'], .product")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".product-image img, .product-card img, .product img")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-name, .product-title, h3, h4, h5, h6")
    PRODUCT_PRICES = (By.XPATH, "//*[contains(text(), 'Ksh')]")
    NEW_BADGES = (By.CSS_SELECTOR, ".new-badge, .badge-new, [class*='new']")
    
    # Product interaction buttons
    ADD_TO_CART_BUTTONS = (By.XPATH, "//button[contains(text(), 'Add to Cart')] | //a[contains(text(), 'Add to Cart')]")
    ADD_TO_WISHLIST_BUTTONS = (By.CSS_SELECTOR, ".wishlist-btn, [class*='wishlist'], .add-to-wishlist")
    QUICK_VIEW_BUTTONS = (By.CSS_SELECTOR, ".quick-view, [class*='quick-view']")
    
    # Filtering options
    CATEGORY_FILTERS = {
        "HEELS": (By.XPATH, "//a[contains(text(), 'HEELS')] | //label[contains(text(), 'HEELS')]"),
        "WEDGES": (By.XPATH, "//a[contains(text(), 'WEDGES')] | //label[contains(text(), 'WEDGES')]"),
        "BOOTS": (By.XPATH, "//a[contains(text(), 'BOOTS')] | //label[contains(text(), 'BOOTS')]"),
        "SANDALS": (By.XPATH, "//a[contains(text(), 'SANDALS')] | //label[contains(text(), 'SANDALS')]"),
        "LOAFERS": (By.XPATH, "//a[contains(text(), 'LOAFERS')] | //label[contains(text(), 'LOAFERS')]"),
        "SNEAKERS": (By.XPATH, "//a[contains(text(), 'SNEAKERS')] | //label[contains(text(), 'SNEAKERS')]")
    }
    
    # Size filters
    SIZE_FILTERS = {
        "35": (By.XPATH, "//a[text()='35'] | //label[text()='35']"),
        "36": (By.XPATH, "//a[text()='36'] | //label[text()='36']"),
        "37": (By.XPATH, "//a[text()='37'] | //label[text()='37']"),
        "38": (By.XPATH, "//a[text()='38'] | //label[text()='38']"),
        "39": (By.XPATH, "//a[text()='39'] | //label[text()='39']"),
        "40": (By.XPATH, "//a[text()='40'] | //label[text()='40']"),
        "41": (By.XPATH, "//a[text()='41'] | //label[text()='41']"),
        "42": (By.XPATH, "//a[text()='42'] | //label[text()='42']"),
        "44": (By.XPATH, "//a[text()='44'] | //label[text()='44']"),
        "46": (By.XPATH, "//a[text()='46'] | //label[text()='46']")
    }
    
    # Sorting options
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[name*='sort'], .sort-select, #sort")
    SORT_OPTIONS = {
        "default": "Default sorting",
        "rating": "Sort by average rating",
        "latest": "Sort by latest",
        "price_low": "Sort by price: low to high",
        "price_high": "Sort by price: high to low"
    }
    
    # Pagination
    PAGINATION = (By.CSS_SELECTOR, ".pagination, .page-numbers")
    PREVIOUS_PAGE = (By.XPATH, "//a[contains(text(), 'Previous')] | //a[contains(@class, 'prev')]")
    NEXT_PAGE = (By.XPATH, "//a[contains(text(), 'Next')] | //a[contains(@class, 'next')]")
    PAGE_NUMBERS = (By.CSS_SELECTOR, ".page-numbers a, .pagination a")
    CURRENT_PAGE = (By.CSS_SELECTOR, ".current, .active, [class*='current'], [class*='active']")
    
    # Search functionality
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], input[name*='search'], .search-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .search-btn, .search-button")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search-results, .results")
    NO_RESULTS_MESSAGE = (By.XPATH, "//*[contains(text(), 'No products found')] | //*[contains(text(), 'no results')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def open_shop_page(self):
        """Open the shop page"""
        self.open_url(Config.BASE_URL + "shop")
        self.wait_for_page_load()
        
    def is_shop_page_loaded(self) -> bool:
        """Check if shop page is loaded"""
        return (
            self.is_element_visible(self.PRODUCT_GRID, timeout=10) or
            self.is_element_visible(self.PRODUCT_CARDS, timeout=10) or
            self.is_element_visible(self.PRODUCTS_COUNT, timeout=10)
        )
        
    def get_products_count_text(self) -> str:
        """Get the products count text"""
        if self.is_element_visible(self.PRODUCTS_COUNT):
            return self.get_element_text(self.PRODUCTS_COUNT)
        return ""
        
    def get_total_products_count(self) -> int:
        """Extract total products count from text"""
        count_text = self.get_products_count_text()
        # Extract number from text like "193 Products found"
        import re
        match = re.search(r'(\d+)', count_text)
        return int(match.group(1)) if match else 0
        
    def get_visible_products_count(self) -> int:
        """Get number of visible product cards"""
        products = self.find_elements(self.PRODUCT_CARDS)
        return len(products)
        
    def get_product_names(self) -> list:
        """Get list of all visible product names"""
        names = []
        name_elements = self.find_elements(self.PRODUCT_NAMES)
        for element in name_elements:
            text = element.text.strip()
            if text and "Ksh" not in text:  # Exclude price text
                names.append(text)
        return names
        
    def get_product_prices(self) -> list:
        """Get list of all visible product prices"""
        prices = []
        price_elements = self.find_elements(self.PRODUCT_PRICES)
        for element in price_elements:
            price_text = element.text.strip()
            if "Ksh" in price_text:
                prices.append(price_text)
        return prices
        
    def click_product_by_name(self, product_name: str):
        """Click on a product by its name"""
        product_locator = (By.XPATH, f"//h3[contains(text(), '{product_name}')] | //h4[contains(text(), '{product_name}')] | //h5[contains(text(), '{product_name}')] | //h6[contains(text(), '{product_name}')]")
        if self.is_element_visible(product_locator):
            self.click_element(product_locator)
        else:
            raise Exception(f"Product '{product_name}' not found")
            
    def add_first_product_to_cart(self):
        """Add first product to cart"""
        cart_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if cart_buttons:
            cart_buttons[0].click()
            logger.info("Added first product to cart")
        else:
            raise Exception("No Add to Cart buttons found")
            
    def add_product_to_cart_by_index(self, index: int):
        """Add product to cart by index (0-based)"""
        cart_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if index < len(cart_buttons):
            cart_buttons[index].click()
            logger.info(f"Added product at index {index} to cart")
        else:
            raise Exception(f"Product index {index} not found")
            
    def add_product_to_wishlist_by_index(self, index: int):
        """Add product to wishlist by index"""
        wishlist_buttons = self.find_elements(self.ADD_TO_WISHLIST_BUTTONS)
        if index < len(wishlist_buttons):
            wishlist_buttons[index].click()
            logger.info(f"Added product at index {index} to wishlist")
        else:
            logger.warning(f"Wishlist button at index {index} not found")
            
    def filter_by_category(self, category: str):
        """Filter products by category"""
        category_upper = category.upper()
        if category_upper in self.CATEGORY_FILTERS:
            locator = self.CATEGORY_FILTERS[category_upper]
            if self.is_element_visible(locator, timeout=5):
                self.click_element(locator)
                self.wait_for_page_load()
            else:
                logger.warning(f"Category filter '{category}' not found")
        else:
            raise ValueError(f"Unsupported category: {category}")
            
    def filter_by_size(self, size: str):
        """Filter products by size"""
        if size in self.SIZE_FILTERS:
            locator = self.SIZE_FILTERS[size]
            if self.is_element_visible(locator, timeout=5):
                self.click_element(locator)
                self.wait_for_page_load()
            else:
                logger.warning(f"Size filter '{size}' not found")
        else:
            raise ValueError(f"Unsupported size: {size}")
            
    def sort_products(self, sort_type: str):
        """Sort products by specified criteria"""
        if self.is_element_visible(self.SORT_DROPDOWN, timeout=5):
            from selenium.webdriver.support.ui import Select
            dropdown = Select(self.find_element(self.SORT_DROPDOWN))
            
            if sort_type in self.SORT_OPTIONS:
                option_text = self.SORT_OPTIONS[sort_type]
                try:
                    dropdown.select_by_visible_text(option_text)
                    self.wait_for_page_load()
                except:
                    logger.warning(f"Could not select sort option: {option_text}")
            else:
                raise ValueError(f"Unsupported sort type: {sort_type}")
        else:
            logger.warning("Sort dropdown not found")
            
    def search_products(self, search_term: str):
        """Search for products"""
        if self.is_element_visible(self.SEARCH_INPUT, timeout=5):
            self.send_keys_to_element(self.SEARCH_INPUT, search_term)
            
            if self.is_element_visible(self.SEARCH_BUTTON, timeout=3):
                self.click_element(self.SEARCH_BUTTON)
            else:
                # Try pressing Enter
                from selenium.webdriver.common.keys import Keys
                search_element = self.find_element(self.SEARCH_INPUT)
                search_element.send_keys(Keys.RETURN)
                
            self.wait_for_page_load()
        else:
            logger.warning("Search input not found")
            
    def go_to_next_page(self):
        """Go to next page of products"""
        if self.is_element_visible(self.NEXT_PAGE, timeout=5):
            self.click_element(self.NEXT_PAGE)
            self.wait_for_page_load()
        else:
            logger.warning("Next page button not found")
            
    def go_to_previous_page(self):
        """Go to previous page of products"""
        if self.is_element_visible(self.PREVIOUS_PAGE, timeout=5):
            self.click_element(self.PREVIOUS_PAGE)
            self.wait_for_page_load()
        else:
            logger.warning("Previous page button not found")
            
    def go_to_page(self, page_number: int):
        """Go to specific page number"""
        page_locator = (By.XPATH, f"//a[text()='{page_number}']")
        if self.is_element_visible(page_locator, timeout=5):
            self.click_element(page_locator)
            self.wait_for_page_load()
        else:
            logger.warning(f"Page {page_number} not found")
            
    def get_current_page_number(self) -> int:
        """Get current page number"""
        if self.is_element_visible(self.CURRENT_PAGE, timeout=5):
            page_text = self.get_element_text(self.CURRENT_PAGE)
            try:
                return int(page_text)
            except ValueError:
                return 1
        return 1
        
    def verify_products_loaded(self) -> bool:
        """Verify that products are loaded on the page"""
        return self.get_visible_products_count() > 0
        
    def verify_no_products_message(self) -> bool:
        """Check if 'no products found' message is displayed"""
        return self.is_element_visible(self.NO_RESULTS_MESSAGE, timeout=5)
