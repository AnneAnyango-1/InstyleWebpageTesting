"""Home page object model"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """Home page object model for instylekenya.co.ke"""
    
    # Locators
    LOGO = (By.CSS_SELECTOR, ".header__logo img, .logo img, [alt*='Instyle'], [alt*='logo']")
    SEARCH_BOX = (By.CSS_SELECTOR, "input[name='q'], .search__input, #search-input, input[placeholder*='Search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']:has(svg), .search__submit, .search-btn")
    MAIN_NAVIGATION = (By.CSS_SELECTOR, ".main-nav, .navigation, .header__nav, nav")
    
    # Navigation menu items
    MENU_DRESSES = (By.CSS_SELECTOR, "a[href*='dress'], a:contains('Dresses')")
    MENU_SHOES = (By.CSS_SELECTOR, "a[href*='shoe'], a:contains('Shoes')")
    MENU_BAGS = (By.CSS_SELECTOR, "a[href*='bag'], a:contains('Bags')")
    MENU_JEWELRY = (By.CSS_SELECTOR, "a[href*='jewelry'], a:contains('Jewelry')")
    MENU_ACCESSORIES = (By.CSS_SELECTOR, "a[href*='accessories'], a:contains('Accessories')")
    
    # User account links
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login'], a:contains('Login'), a:contains('Sign In')")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href*='register'], a:contains('Register'), a:contains('Sign Up')")
    ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href*='account'], .account-link")
    
    # Cart and wishlist
    CART_LINK = (By.CSS_SELECTOR, "a[href*='cart'], .cart-link, .header__cart")
    WISHLIST_LINK = (By.CSS_SELECTOR, "a[href*='wishlist'], .wishlist-link")
    CART_COUNT = (By.CSS_SELECTOR, ".cart-count, .cart__count, .header__cart-count")
    
    # Hero/Banner section
    HERO_SECTION = (By.CSS_SELECTOR, ".hero, .banner, .slideshow, .main-banner")
    HERO_TITLE = (By.CSS_SELECTOR, ".hero__title, .banner__title, .slideshow__title")
    HERO_CTA_BUTTON = (By.CSS_SELECTOR, ".hero__cta, .banner__cta, .btn--primary")
    
    # Product sections
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".featured-products, .product-grid, .collection-grid")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card, .product-item, .grid__item")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-card__title, .product__title, .product-title")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-card__price, .product__price, .price")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".product-card__image img, .product__image img")
    
    # Footer
    FOOTER = (By.CSS_SELECTOR, "footer, .footer")
    FOOTER_LINKS = (By.CSS_SELECTOR, "footer a, .footer a")
    
    # Newsletter signup
    NEWSLETTER_INPUT = (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    NEWSLETTER_SUBMIT = (By.CSS_SELECTOR, "button[type='submit']:has-text('Subscribe'), .newsletter__submit")
    
    # Social media links
    SOCIAL_LINKS = (By.CSS_SELECTOR, ".social a, .social-links a, a[href*='facebook'], a[href*='instagram'], a[href*='twitter']")
    
    def __init__(self, driver):
        """Initialize home page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
    def load(self):
        """Load the home page"""
        self.go_to(Config.URLS["home"])
        return self
    
    def is_loaded(self) -> bool:
        """Check if home page is loaded
        
        Returns:
            True if page is loaded, False otherwise
        """
        return self.is_element_visible(self.LOGO) and "instyle" in self.get_page_title().lower()
    
    def search_for_product(self, search_term: str) -> bool:
        """Search for a product
        
        Args:
            search_term: Term to search for
            
        Returns:
            True if search was successful, False otherwise
        """
        try:
            # Click on search box and enter search term
            if self.send_keys_to_element(self.SEARCH_BOX, search_term):
                # Click search button or press enter
                if self.click_element(self.SEARCH_BUTTON):
                    self.wait_for_page_load()
                    return True
                else:
                    # Try pressing Enter as fallback
                    from selenium.webdriver.common.keys import Keys
                    search_box = self.find_element(self.SEARCH_BOX)
                    search_box.send_keys(Keys.RETURN)
                    self.wait_for_page_load()
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to search for product '{search_term}': {str(e)}")
            return False
    
    def get_featured_products(self) -> list:
        """Get list of featured products on homepage
        
        Returns:
            List of product information dictionaries
        """
        products = []
        try:
            product_cards = self.find_elements(self.PRODUCT_CARDS)
            
            for card in product_cards[:10]:  # Limit to first 10 products
                try:
                    # Get product title
                    title_element = card.find_element(*self.PRODUCT_TITLES)
                    title = title_element.text if title_element else "No title"
                    
                    # Get product price
                    price_element = card.find_element(*self.PRODUCT_PRICES)
                    price = price_element.text if price_element else "No price"
                    
                    # Get product image
                    image_element = card.find_element(*self.PRODUCT_IMAGES)
                    image_src = image_element.get_attribute("src") if image_element else ""
                    
                    products.append({
                        "title": title,
                        "price": price,
                        "image_src": image_src
                    })
                except Exception as e:
                    logger.warning(f"Could not extract product info: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to get featured products: {str(e)}")
            
        return products
    
    def click_product_category(self, category: str) -> bool:
        """Click on a product category in navigation
        
        Args:
            category: Category name (dresses, shoes, bags, jewelry, accessories)
            
        Returns:
            True if category was clicked, False otherwise
        """
        category_locators = {
            "dresses": self.MENU_DRESSES,
            "shoes": self.MENU_SHOES,
            "bags": self.MENU_BAGS,
            "jewelry": self.MENU_JEWELRY,
            "accessories": self.MENU_ACCESSORIES
        }
        
        category_key = category.lower()
        if category_key in category_locators:
            if self.click_element(category_locators[category_key]):
                self.wait_for_page_load()
                return True
        
        logger.error(f"Could not click category: {category}")
        return False
    
    def click_login_link(self) -> bool:
        """Click on login link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.LOGIN_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def click_register_link(self) -> bool:
        """Click on register link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.REGISTER_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def click_cart_link(self) -> bool:
        """Click on cart link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.CART_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def click_wishlist_link(self) -> bool:
        """Click on wishlist link
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.WISHLIST_LINK):
            self.wait_for_page_load()
            return True
        return False
    
    def get_cart_item_count(self) -> str:
        """Get the cart item count
        
        Returns:
            Cart count as string, or '0' if not found
        """
        try:
            return self.get_element_text(self.CART_COUNT) or "0"
        except:
            return "0"
    
    def is_hero_section_visible(self) -> bool:
        """Check if hero section is visible
        
        Returns:
            True if hero section is visible, False otherwise
        """
        return self.is_element_visible(self.HERO_SECTION)
    
    def get_hero_title(self) -> str:
        """Get hero section title
        
        Returns:
            Hero title text
        """
        return self.get_element_text(self.HERO_TITLE)
    
    def click_hero_cta(self) -> bool:
        """Click hero call-to-action button
        
        Returns:
            True if clicked successfully, False otherwise
        """
        return self.click_element(self.HERO_CTA_BUTTON)
    
    def get_navigation_links(self) -> list:
        """Get all navigation links
        
        Returns:
            List of navigation link texts
        """
        try:
            nav_element = self.find_element(self.MAIN_NAVIGATION)
            links = nav_element.find_elements(By.TAG_NAME, "a")
            return [link.text for link in links if link.text.strip()]
        except Exception as e:
            logger.error(f"Could not get navigation links: {str(e)}")
            return []
    
    def subscribe_to_newsletter(self, email: str) -> bool:
        """Subscribe to newsletter
        
        Args:
            email: Email address to subscribe
            
        Returns:
            True if subscription was successful, False otherwise
        """
        try:
            if self.send_keys_to_element(self.NEWSLETTER_INPUT, email):
                return self.click_element(self.NEWSLETTER_SUBMIT)
            return False
        except Exception as e:
            logger.error(f"Failed to subscribe to newsletter: {str(e)}")
            return False
    
    def get_social_media_links(self) -> list:
        """Get all social media links
        
        Returns:
            List of social media URLs
        """
        try:
            social_elements = self.find_elements(self.SOCIAL_LINKS)
            return [link.get_attribute("href") for link in social_elements if link.get_attribute("href")]
        except Exception as e:
            logger.error(f"Could not get social media links: {str(e)}")
            return []
