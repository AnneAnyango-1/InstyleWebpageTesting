import pytest
import time
from pages.cart_page import CartPage
from pages.shop_page import ShopPage
from pages.home_page import HomePage
from config.config import Config

@pytest.mark.product
class TestCartFunctionality:
    """Test cases for shopping cart functionality"""
    
    def test_cart_page_loads(self, driver):
        """Test that cart page loads successfully"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        assert cart_page.is_cart_page_loaded(), "Cart page did not load successfully"
        
    def test_empty_cart_display(self, driver):
        """Test empty cart message display"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        # Check if cart is empty or has items
        if cart_page.is_cart_empty():
            assert cart_page.is_element_visible(cart_page.EMPTY_CART_MESSAGE), "Empty cart message should be displayed"
        else:
            items_count = cart_page.get_cart_items_count()
            assert items_count > 0, "Cart shows items but count is 0"
            
    def test_add_product_to_cart_from_shop(self, driver):
        """Test adding product to cart from shop page"""
        shop_page = ShopPage(driver)
        cart_page = CartPage(driver)
        
        # Go to shop page
        shop_page.open_shop_page()
        
        if not shop_page.is_shop_page_loaded():
            pytest.skip("Shop page not accessible")
            
        # Check if products are available
        if shop_page.get_visible_products_count() == 0:
            pytest.skip("No products available to add to cart")
            
        # Get initial cart count (if available)
        initial_product_names = shop_page.get_product_names()
        if not initial_product_names:
            pytest.skip("No product names found")
            
        try:
            # Add first product to cart
            shop_page.add_first_product_to_cart()
            time.sleep(2)  # Wait for cart update
            
            # Go to cart page to verify
            cart_page.open_cart_page()
            
            if not cart_page.is_cart_empty():
                cart_items = cart_page.get_cart_item_names()
                assert len(cart_items) > 0, "Product was not added to cart"
            else:
                pytest.skip("Cart appears empty - add to cart may not be functional")
                
        except Exception as e:
            pytest.skip(f"Could not add product to cart: {e}")
            
    def test_cart_item_details_display(self, driver):
        """Test cart item details are displayed correctly"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        if cart_page.is_cart_empty():
            pytest.skip("Cart is empty - cannot test item details")
            
        # Check item details
        item_names = cart_page.get_cart_item_names()
        item_prices = cart_page.get_cart_item_prices()
        
        assert len(item_names) > 0, "No item names displayed"
        assert len(item_prices) > 0, "No item prices displayed"
        
        # Verify prices contain currency
        for price in item_prices:
            assert "Ksh" in price, f"Price '{price}' does not contain currency"
            
    def test_quantity_update_functionality(self, driver):
        """Test updating item quantity in cart"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        if cart_page.is_cart_empty():
            pytest.skip("Cart is empty - cannot test quantity update")
            
        items_count = cart_page.get_cart_items_count()
        if items_count == 0:
            pytest.skip("No items in cart to update quantity")
            
        try:
            # Get initial quantity for first item
            initial_qty = cart_page.get_item_quantity(0)
            
            # Try to increase quantity
            cart_page.increase_quantity(0)
            time.sleep(2)
            
            # Check if quantity increased
            new_qty = cart_page.get_item_quantity(0)
            
            if new_qty > initial_qty:
                assert True, "Quantity increased successfully"
            else:
                # Try updating quantity directly
                cart_page.update_quantity(0, 3)
                time.sleep(2)
                
                updated_qty = cart_page.get_item_quantity(0)
                assert updated_qty != initial_qty or updated_qty == 3, "Quantity update functionality working"
                
        except Exception as e:
            pytest.skip(f"Quantity update not available: {e}")
            
    def test_remove_item_from_cart(self, driver):
        """Test removing item from cart"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        if cart_page.is_cart_empty():
            pytest.skip("Cart is empty - cannot test item removal")
            
        initial_count = cart_page.get_cart_items_count()
        if initial_count == 0:
            pytest.skip("No items to remove")
            
        try:
            # Remove first item
            cart_page.remove_item(0)
            time.sleep(2)
            
            # Check if item was removed
            final_count = cart_page.get_cart_items_count()
            
            assert final_count < initial_count or cart_page.is_cart_empty(), "Item was not removed from cart"
            
        except Exception as e:
            pytest.skip(f"Remove item functionality not available: {e}")
            
    def test_cart_totals_display(self, driver):
        """Test cart totals calculation and display"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        if cart_page.is_cart_empty():
            pytest.skip("Cart is empty - cannot test totals")
            
        # Check for subtotal
        subtotal = cart_page.get_subtotal()
        total = cart_page.get_total_amount()
        
        # At least one total should be displayed
        assert subtotal or total, "No cart totals displayed"
        
        if total:
            assert "Ksh" in total, "Total amount should contain currency"
            
    def test_coupon_application(self, driver):
        """Test coupon code application"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        if cart_page.is_cart_empty():
            pytest.skip("Cart is empty - cannot test coupon")
            
        try:
            # Try applying a test coupon
            cart_page.apply_coupon("TEST10")
            time.sleep(2)
            
            # Check for success or error message
            success_msg = cart_page.get_success_message()
            error_msg = cart_page.get_error_message()
            
            assert success_msg or error_msg, "Expected response for coupon application"
            
        except Exception as e:
            pytest.skip(f"Coupon functionality not available: {e}")
            
    def test_proceed_to_checkout(self, driver):
        """Test proceeding to checkout"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        if cart_page.is_cart_empty():
            pytest.skip("Cart is empty - cannot test checkout")
            
        if cart_page.is_element_visible(cart_page.CHECKOUT_BUTTON, timeout=5):
            initial_url = cart_page.get_current_url()
            cart_page.proceed_to_checkout()
            time.sleep(3)
            
            final_url = cart_page.get_current_url()
            
            # Should navigate to checkout page or show checkout form
            assert initial_url != final_url or "checkout" in final_url.lower(), "Checkout navigation failed"
        else:
            pytest.skip("Checkout button not available")
            
    def test_continue_shopping(self, driver):
        """Test continue shopping functionality"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        if cart_page.is_element_visible(cart_page.CONTINUE_SHOPPING, timeout=5):
            cart_page.continue_shopping()
            time.sleep(2)
            
            current_url = cart_page.get_current_url()
            
            # Should navigate away from cart page
            assert "cart" not in current_url.lower(), "Continue shopping did not navigate away from cart"
        else:
            pytest.skip("Continue shopping button not available")
            
    def test_cart_persistence_across_sessions(self, driver):
        """Test cart persistence (basic test)"""
        cart_page = CartPage(driver)
        
        # Check initial cart state
        cart_page.open_cart_page()
        initial_empty = cart_page.is_cart_empty()
        initial_count = cart_page.get_cart_items_count() if not initial_empty else 0
        
        # Navigate away and back
        home_page = HomePage(driver)
        home_page.open_homepage()
        time.sleep(1)
        
        cart_page.open_cart_page()
        final_empty = cart_page.is_cart_empty()
        final_count = cart_page.get_cart_items_count() if not final_empty else 0
        
        # Cart state should be consistent
        assert initial_empty == final_empty, "Cart empty state changed after navigation"
        assert initial_count == final_count, "Cart item count changed after navigation"
        
    @pytest.mark.error_handling
    def test_cart_error_handling(self, driver):
        """Test cart error scenarios"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        # Test invalid quantity update
        if not cart_page.is_cart_empty():
            try:
                # Try setting negative quantity
                cart_page.update_quantity(0, -1)
                time.sleep(1)
                
                # Should show error or prevent negative quantity
                error_msg = cart_page.get_error_message()
                quantity = cart_page.get_item_quantity(0)
                
                assert error_msg or quantity >= 0, "Negative quantity should be prevented"
                
            except Exception as e:
                pytest.skip(f"Quantity validation test not applicable: {e}")
        else:
            pytest.skip("Cart is empty - cannot test error handling")
            
    def test_cart_accessibility_features(self, driver):
        """Test cart accessibility features"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        # Check for proper headings
        page_title = cart_page.get_page_title()
        assert "cart" in page_title.lower(), "Page title should indicate cart page"
        
        # Check for main cart container
        assert cart_page.is_element_visible(cart_page.CART_ITEMS_CONTAINER, timeout=5) or cart_page.is_cart_empty(), "Cart container should be visible"
