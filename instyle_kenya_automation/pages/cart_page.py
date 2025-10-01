"""Cart page object model"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class CartPage(BasePage):
    """Cart page object model for instylekenya.co.ke"""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart__item, .cart-item, .line-item")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".cart__item-title, .cart-item__title, .line-item__title")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".cart__item-price, .cart-item__price, .line-item__price")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".cart__item-image img, .cart-item__image img")
    
    # Quantity controls
    QUANTITY_INPUTS = (By.CSS_SELECTOR, "input[name*='quantity'], .quantity__input, .cart__quantity-input")
    QUANTITY_INCREASE_BUTTONS = (By.CSS_SELECTOR, ".quantity__button--increase, .qty-plus, .quantity-plus")
    QUANTITY_DECREASE_BUTTONS = (By.CSS_SELECTOR, ".quantity__button--decrease, .qty-minus, .quantity-minus")
    UPDATE_QUANTITY_BUTTONS = (By.CSS_SELECTOR, "button[name*='update'], .cart__update")
    
    # Remove items
    REMOVE_ITEM_BUTTONS = (By.CSS_SELECTOR, ".cart__remove, .remove-item, a[href*='remove'], button[name*='remove']")
    
    # Cart totals
    SUBTOTAL = (By.CSS_SELECTOR, ".cart__subtotal, .subtotal, .cart-subtotal")
    SHIPPING_COST = (By.CSS_SELECTOR, ".cart__shipping, .shipping-cost")
    TAX_AMOUNT = (By.CSS_SELECTOR, ".cart__tax, .tax-amount")
    TOTAL_AMOUNT = (By.CSS_SELECTOR, ".cart__total, .total-amount, .grand-total")
    
    # Checkout elements
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "button[name='add'], .btn--checkout, .cart__checkout, a[href*='checkout']")
    CONTINUE_SHOPPING_LINK = (By.CSS_SELECTOR, ".continue-shopping, a[href*='continue'], .cart__continue")
    
    # Empty cart
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".cart--empty, .empty-cart, .cart__empty")
    EMPTY_CART_LINK = (By.CSS_SELECTOR, ".cart__empty-link, .empty-cart__link")
    
    # Shipping calculator
    SHIPPING_CALCULATOR = (By.CSS_SELECTOR, ".shipping-calculator, .cart__shipping-calculator")
    COUNTRY_SELECT = (By.CSS_SELECTOR, "select[name*='country'], #shipping_country")
    STATE_SELECT = (By.CSS_SELECTOR, "select[name*='state'], select[name*='province'], #shipping_state")
    ZIP_INPUT = (By.CSS_SELECTOR, "input[name*='zip'], input[name*='postal'], #shipping_zip")
    CALCULATE_SHIPPING_BUTTON = (By.CSS_SELECTOR, "button[name*='shipping'], .calculate-shipping")
    
    # Discount/Coupon
    COUPON_INPUT = (By.CSS_SELECTOR, "input[name*='coupon'], input[name*='discount'], #coupon_code")
    APPLY_COUPON_BUTTON = (By.CSS_SELECTOR, "button[name*='coupon'], .apply-coupon")
    COUPON_ERROR = (By.CSS_SELECTOR, ".coupon-error, .discount-error")
    COUPON_SUCCESS = (By.CSS_SELECTOR, ".coupon-success, .discount-success")
    
    # Notes
    ORDER_NOTES = (By.CSS_SELECTOR, "textarea[name*='note'], #order_notes, .cart__notes")
    
    def __init__(self, driver):
        """Initialize cart page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
    def load(self):
        """Load the cart page"""
        self.go_to(Config.URLS["cart"])
        return self
    
    def is_loaded(self) -> bool:
        """Check if cart page is loaded
        
        Returns:
            True if page is loaded, False otherwise
        """
        return ("cart" in self.get_current_url().lower() or 
                self.is_element_present(self.CART_ITEMS) or 
                self.is_element_present(self.EMPTY_CART_MESSAGE))
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty
        
        Returns:
            True if cart is empty, False otherwise
        """
        return (self.is_element_visible(self.EMPTY_CART_MESSAGE) or 
                len(self.find_elements(self.CART_ITEMS)) == 0)
    
    def get_cart_items(self) -> list:
        """Get all items in the cart
        
        Returns:
            List of cart item dictionaries
        """
        items = []
        try:
            cart_items = self.find_elements(self.CART_ITEMS)
            
            for item in cart_items:
                try:
                    # Get product name
                    name_element = item.find_element(*self.PRODUCT_NAMES)
                    name = name_element.text if name_element else "Unknown Product"
                    
                    # Get product price
                    price_element = item.find_element(*self.PRODUCT_PRICES)
                    price = price_element.text if price_element else "$0.00"
                    
                    # Get quantity
                    quantity_element = item.find_element(*self.QUANTITY_INPUTS)
                    quantity = quantity_element.get_attribute("value") if quantity_element else "1"
                    
                    # Get image src
                    image_element = item.find_element(*self.PRODUCT_IMAGES)
                    image_src = image_element.get_attribute("src") if image_element else ""
                    
                    items.append({
                        "name": name,
                        "price": price,
                        "quantity": quantity,
                        "image_src": image_src
                    })
                    
                except Exception as e:
                    logger.warning(f"Could not extract item info: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to get cart items: {str(e)}")
            
        return items
    
    def get_cart_item_count(self) -> int:
        """Get the number of items in cart
        
        Returns:
            Number of cart items
        """
        try:
            return len(self.find_elements(self.CART_ITEMS))
        except Exception:
            return 0
    
    def update_item_quantity(self, item_index: int, new_quantity: int) -> bool:
        """Update quantity for a specific cart item
        
        Args:
            item_index: Index of the item (0-based)
            new_quantity: New quantity value
            
        Returns:
            True if quantity was updated, False otherwise
        """
        try:
            quantity_inputs = self.find_elements(self.QUANTITY_INPUTS)
            
            if item_index < len(quantity_inputs):
                quantity_input = quantity_inputs[item_index]
                quantity_input.clear()
                quantity_input.send_keys(str(new_quantity))
                
                # Look for update button
                update_buttons = self.find_elements(self.UPDATE_QUANTITY_BUTTONS)
                if update_buttons and item_index < len(update_buttons):
                    update_buttons[item_index].click()
                else:
                    # Try pressing Enter if no update button
                    from selenium.webdriver.common.keys import Keys
                    quantity_input.send_keys(Keys.RETURN)
                
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to update quantity: {str(e)}")
            return False
    
    def increase_item_quantity(self, item_index: int) -> bool:
        """Increase quantity for a specific cart item
        
        Args:
            item_index: Index of the item (0-based)
            
        Returns:
            True if quantity was increased, False otherwise
        """
        try:
            increase_buttons = self.find_elements(self.QUANTITY_INCREASE_BUTTONS)
            
            if item_index < len(increase_buttons):
                increase_buttons[item_index].click()
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to increase quantity: {str(e)}")
            return False
    
    def decrease_item_quantity(self, item_index: int) -> bool:
        """Decrease quantity for a specific cart item
        
        Args:
            item_index: Index of the item (0-based)
            
        Returns:
            True if quantity was decreased, False otherwise
        """
        try:
            decrease_buttons = self.find_elements(self.QUANTITY_DECREASE_BUTTONS)
            
            if item_index < len(decrease_buttons):
                decrease_buttons[item_index].click()
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to decrease quantity: {str(e)}")
            return False
    
    def remove_item(self, item_index: int) -> bool:
        """Remove a specific item from cart
        
        Args:
            item_index: Index of the item to remove (0-based)
            
        Returns:
            True if item was removed, False otherwise
        """
        try:
            remove_buttons = self.find_elements(self.REMOVE_ITEM_BUTTONS)
            
            if item_index < len(remove_buttons):
                remove_buttons[item_index].click()
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to remove item: {str(e)}")
            return False
    
    def get_subtotal(self) -> str:
        """Get cart subtotal
        
        Returns:
            Subtotal amount as string
        """
        return self.get_element_text(self.SUBTOTAL)
    
    def get_shipping_cost(self) -> str:
        """Get shipping cost
        
        Returns:
            Shipping cost as string
        """
        return self.get_element_text(self.SHIPPING_COST)
    
    def get_tax_amount(self) -> str:
        """Get tax amount
        
        Returns:
            Tax amount as string
        """
        return self.get_element_text(self.TAX_AMOUNT)
    
    def get_total_amount(self) -> str:
        """Get total cart amount
        
        Returns:
            Total amount as string
        """
        return self.get_element_text(self.TOTAL_AMOUNT)
    
    def proceed_to_checkout(self) -> bool:
        """Click proceed to checkout button
        
        Returns:
            True if clicked successfully, False otherwise
        """
        if self.click_element(self.CHECKOUT_BUTTON):
            self.wait_for_page_load()
            return True
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
    
    def apply_coupon(self, coupon_code: str) -> bool:
        """Apply a coupon code
        
        Args:
            coupon_code: Coupon code to apply
            
        Returns:
            True if coupon was applied successfully, False otherwise
        """
        try:
            if self.send_keys_to_element(self.COUPON_INPUT, coupon_code):
                if self.click_element(self.APPLY_COUPON_BUTTON):
                    self.wait_for_page_load()
                    
                    # Check for success or error messages
                    if self.is_element_visible(self.COUPON_SUCCESS, timeout=5):
                        return True
                    elif self.is_element_visible(self.COUPON_ERROR, timeout=5):
                        return False
                    
                    return True  # Assume success if no explicit message
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to apply coupon: {str(e)}")
            return False
    
    def get_coupon_error_message(self) -> str:
        """Get coupon error message
        
        Returns:
            Error message or empty string
        """
        return self.get_element_text(self.COUPON_ERROR)
    
    def calculate_shipping(self, country: str = None, state: str = None, zip_code: str = None) -> bool:
        """Calculate shipping cost
        
        Args:
            country: Country name or code
            state: State/province name or code
            zip_code: ZIP/postal code
            
        Returns:
            True if shipping was calculated, False otherwise
        """
        try:
            if not self.is_element_present(self.SHIPPING_CALCULATOR):
                return False
            
            # Select country if provided
            if country and self.is_element_present(self.COUNTRY_SELECT):
                from selenium.webdriver.support.ui import Select
                country_dropdown = Select(self.find_element(self.COUNTRY_SELECT))
                country_dropdown.select_by_visible_text(country)
            
            # Select state if provided
            if state and self.is_element_present(self.STATE_SELECT):
                from selenium.webdriver.support.ui import Select
                state_dropdown = Select(self.find_element(self.STATE_SELECT))
                state_dropdown.select_by_visible_text(state)
            
            # Enter ZIP code if provided
            if zip_code and self.is_element_present(self.ZIP_INPUT):
                self.send_keys_to_element(self.ZIP_INPUT, zip_code)
            
            # Click calculate button
            if self.click_element(self.CALCULATE_SHIPPING_BUTTON):
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to calculate shipping: {str(e)}")
            return False
    
    def add_order_notes(self, notes: str) -> bool:
        """Add notes to the order
        
        Args:
            notes: Order notes text
            
        Returns:
            True if notes were added, False otherwise
        """
        try:
            return self.send_keys_to_element(self.ORDER_NOTES, notes)
        except Exception as e:
            logger.error(f"Failed to add order notes: {str(e)}")
            return False
    
    def get_empty_cart_message(self) -> str:
        """Get empty cart message
        
        Returns:
            Empty cart message text
        """
        return self.get_element_text(self.EMPTY_CART_MESSAGE)
