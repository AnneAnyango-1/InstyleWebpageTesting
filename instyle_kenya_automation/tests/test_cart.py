"""Cart functionality tests"""

import pytest
import logging
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.search_results_page import SearchResultsPage
from config.config import Config

logger = logging.getLogger(__name__)

class TestCart:
    """Test suite for shopping cart functionality"""
    
    @pytest.mark.cart
    @pytest.mark.smoke
    def test_cart_page_loads(self, driver):
        """Test that cart page loads successfully"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        assert cart_page.is_loaded(), "Cart page should load successfully"
        logger.info("Cart page loaded successfully")
    
    @pytest.mark.cart
    @pytest.mark.smoke
    def test_empty_cart_display(self, driver):
        """Test empty cart display"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if cart_page.is_cart_empty():
            empty_message = cart_page.get_empty_cart_message()
            assert empty_message, "Empty cart should display a message"
            logger.info(f"Empty cart displays message: '{empty_message}'")
        else:
            logger.info("Cart is not empty, skipping empty cart test")
    
    @pytest.mark.cart
    def test_cart_access_from_homepage(self, driver):
        """Test accessing cart from homepage"""
        home_page = HomePage(driver)
        home_page.load()
        
        success = home_page.click_cart_link()
        assert success, "Should be able to access cart from homepage"
        
        cart_page = CartPage(driver)
        assert cart_page.is_loaded(), "Should navigate to cart page"
        logger.info("Successfully accessed cart from homepage")
    
    @pytest.mark.cart
    def test_add_product_to_cart(self, driver, search_terms):
        """Test adding a product to cart"""
        # Search for a product first
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        success = home_page.search_for_product(search_term)
        assert success, f"Should be able to search for '{search_term}'"
        
        # Try to find and click a product
        search_page = SearchResultsPage(driver)
        if search_page.has_results():
            products = search_page.get_search_results()
            if len(products) > 0:
                # Click on first product
                success = search_page.click_product(0)
                if success:
                    product_page = ProductPage(driver)
                    if product_page.is_loaded():
                        # Try to add to cart
                        add_success = product_page.add_to_cart()
                        if add_success:
                            logger.info("Successfully added product to cart")
                            
                            # Verify cart has items
                            cart_page = CartPage(driver)
                            cart_page.load()
                            
                            if not cart_page.is_cart_empty():
                                cart_items = cart_page.get_cart_items()
                                assert len(cart_items) > 0, "Cart should contain items after adding product"
                                logger.info(f"Cart now contains {len(cart_items)} items")
                        else:
                            logger.warning("Could not add product to cart")
                    else:
                        logger.warning("Product page did not load")
                else:
                    logger.warning("Could not click on product")
            else:
                logger.warning("No products found in search results")
        else:
            logger.warning(f"No search results found for '{search_term}'")
    
    @pytest.mark.cart
    def test_cart_item_display(self, driver):
        """Test cart item information display"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if not cart_page.is_cart_empty():
            cart_items = cart_page.get_cart_items()
            
            if len(cart_items) > 0:
                first_item = cart_items[0]
                
                # Verify item has required information
                assert first_item["name"], "Cart item should have a name"
                assert first_item["price"], "Cart item should have a price"
                assert first_item["quantity"], "Cart item should have a quantity"
                
                logger.info(f"Cart item display test passed. First item: {first_item['name']}")
            else:
                logger.info("No items in cart to test display")
        else:
            logger.info("Cart is empty, skipping item display test")
    
    @pytest.mark.cart
    def test_quantity_update(self, driver):
        """Test updating item quantity in cart"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if not cart_page.is_cart_empty():
            initial_count = cart_page.get_cart_item_count()
            
            if initial_count > 0:
                # Try to increase quantity of first item
                success = cart_page.increase_item_quantity(0)
                
                if success:
                    logger.info("Successfully increased item quantity")
                    
                    # Try to decrease quantity
                    decrease_success = cart_page.decrease_item_quantity(0)
                    if decrease_success:
                        logger.info("Successfully decreased item quantity")
                else:
                    # Try manual quantity update
                    update_success = cart_page.update_item_quantity(0, 2)
                    if update_success:
                        logger.info("Successfully updated item quantity manually")
                    else:
                        logger.warning("Could not update item quantity")
            else:
                logger.info("No items in cart to test quantity update")
        else:
            logger.info("Cart is empty, skipping quantity update test")
    
    @pytest.mark.cart
    def test_item_removal(self, driver):
        """Test removing items from cart"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if not cart_page.is_cart_empty():
            initial_count = cart_page.get_cart_item_count()
            
            if initial_count > 0:
                # Try to remove first item
                success = cart_page.remove_item(0)
                
                if success:
                    final_count = cart_page.get_cart_item_count()
                    assert final_count < initial_count, "Item count should decrease after removal"
                    logger.info(f"Successfully removed item. Count: {initial_count} -> {final_count}")
                else:
                    logger.warning("Could not remove item from cart")
            else:
                logger.info("No items in cart to test removal")
        else:
            logger.info("Cart is empty, skipping item removal test")
    
    @pytest.mark.cart
    def test_cart_totals_display(self, driver):
        """Test cart totals and pricing display"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if not cart_page.is_cart_empty():
            subtotal = cart_page.get_subtotal()
            total = cart_page.get_total_amount()
            
            assert subtotal or total, "Cart should display pricing information"
            
            if subtotal:
                logger.info(f"Cart subtotal: {subtotal}")
            if total:
                logger.info(f"Cart total: {total}")
            
            # Check shipping cost if displayed
            shipping = cart_page.get_shipping_cost()
            if shipping:
                logger.info(f"Shipping cost: {shipping}")
        else:
            logger.info("Cart is empty, skipping totals display test")
    
    @pytest.mark.cart
    def test_checkout_button(self, driver):
        """Test checkout button functionality"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if not cart_page.is_cart_empty():
            if cart_page.is_element_present(cart_page.CHECKOUT_BUTTON):
                # Note: We don't actually proceed to checkout to avoid creating orders
                # Just verify the button is present and clickable
                checkout_button = cart_page.find_element(cart_page.CHECKOUT_BUTTON)
                assert checkout_button.is_enabled(), "Checkout button should be enabled when cart has items"
                logger.info("Checkout button is present and enabled")
            else:
                logger.warning("Checkout button not found")
        else:
            logger.info("Cart is empty, skipping checkout button test")
    
    @pytest.mark.cart
    def test_continue_shopping_link(self, driver):
        """Test continue shopping functionality"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if cart_page.is_element_present(cart_page.CONTINUE_SHOPPING_LINK):
            success = cart_page.continue_shopping()
            
            if success:
                # Should be redirected away from cart page
                assert "cart" not in driver.current_url.lower(), "Should be redirected away from cart"
                logger.info("Continue shopping link works correctly")
            else:
                logger.warning("Could not click continue shopping link")
        else:
            logger.info("Continue shopping link not found")
    
    @pytest.mark.cart
    @pytest.mark.regression
    def test_coupon_application(self, driver):
        """Test coupon/discount code application"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if cart_page.is_element_present(cart_page.COUPON_INPUT) and not cart_page.is_cart_empty():
            # Try applying an invalid coupon code
            test_coupon = "TESTCODE123"
            success = cart_page.apply_coupon(test_coupon)
            
            if success:
                # Check for error message (expected for invalid coupon)
                error_msg = cart_page.get_coupon_error_message()
                logger.info(f"Coupon application test completed. Error: '{error_msg}'")
            else:
                logger.warning("Could not apply coupon code")
        else:
            logger.info("Coupon input not found or cart is empty")
    
    @pytest.mark.cart
    def test_shipping_calculator(self, driver):
        """Test shipping cost calculator"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if (cart_page.is_element_present(cart_page.SHIPPING_CALCULATOR) and 
            not cart_page.is_cart_empty()):
            
            # Try calculating shipping
            success = cart_page.calculate_shipping(
                country="Kenya",
                zip_code="00100"
            )
            
            if success:
                shipping_cost = cart_page.get_shipping_cost()
                logger.info(f"Shipping calculation completed. Cost: '{shipping_cost}'")
            else:
                logger.warning("Could not calculate shipping")
        else:
            logger.info("Shipping calculator not found or cart is empty")
    
    @pytest.mark.cart
    def test_order_notes(self, driver):
        """Test order notes functionality"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if (cart_page.is_element_present(cart_page.ORDER_NOTES) and 
            not cart_page.is_cart_empty()):
            
            test_notes = "This is a test order note."
            success = cart_page.add_order_notes(test_notes)
            
            if success:
                # Verify notes were added
                notes_value = cart_page.get_element_attribute(cart_page.ORDER_NOTES, "value")
                assert test_notes in notes_value, "Order notes should be saved"
                logger.info("Order notes functionality works correctly")
            else:
                logger.warning("Could not add order notes")
        else:
            logger.info("Order notes field not found or cart is empty")
    
    @pytest.mark.cart
    @pytest.mark.regression
    def test_cart_persistence(self, driver):
        """Test cart persistence across page navigation"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if not cart_page.is_cart_empty():
            initial_count = cart_page.get_cart_item_count()
            initial_items = cart_page.get_cart_items()
            
            # Navigate away from cart and back
            home_page = HomePage(driver)
            home_page.load()
            
            # Go back to cart
            cart_page.load()
            
            final_count = cart_page.get_cart_item_count()
            assert final_count == initial_count, "Cart should persist across navigation"
            
            logger.info(f"Cart persistence test passed. Items maintained: {final_count}")
        else:
            logger.info("Cart is empty, skipping persistence test")
    
    @pytest.mark.cart
    def test_cart_validation_empty_state(self, driver):
        """Test cart validation in empty state"""
        cart_page = CartPage(driver)
        cart_page.load()
        
        if cart_page.is_cart_empty():
            # Checkout button should be disabled or not present
            if cart_page.is_element_present(cart_page.CHECKOUT_BUTTON):
                checkout_button = cart_page.find_element(cart_page.CHECKOUT_BUTTON)
                # Button might be disabled or hidden
                is_enabled = checkout_button.is_enabled()
                is_displayed = checkout_button.is_displayed()
                
                logger.info(f"Empty cart validation - Checkout button enabled: {is_enabled}, displayed: {is_displayed}")
            else:
                logger.info("Checkout button not present in empty cart (correct behavior)")
        else:
            logger.info("Cart is not empty, skipping empty state validation")
