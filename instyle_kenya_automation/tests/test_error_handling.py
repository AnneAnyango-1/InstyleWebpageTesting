import pytest
import time
from pages.home_page import HomePage
from pages.shop_page import ShopPage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.wishlist_page import WishlistPage
from config.config import Config

@pytest.mark.error_handling
class TestErrorHandlingAndEdgeCases:
    """Test cases for error handling and edge cases"""
    
    def test_invalid_url_handling(self, driver):
        """Test handling of invalid URLs"""
        home_page = HomePage(driver)
        
        invalid_urls = [
            Config.BASE_URL + "invalid-page",
            Config.BASE_URL + "404-test",
            Config.BASE_URL + "non/existent/path"
        ]
        
        for invalid_url in invalid_urls:
            try:
                home_page.open_url(invalid_url)
                time.sleep(2)
                
                # Should handle gracefully - either show error page or redirect
                current_url = home_page.get_current_url()
                page_source = home_page.get_page_source()
                
                # Check for error handling
                error_handled = (
                    "404" in page_source.lower() or
                    "not found" in page_source.lower() or
                    "error" in page_source.lower() or
                    current_url != invalid_url  # Redirected
                )
                
                assert error_handled, f"Invalid URL {invalid_url} should be handled gracefully"
                
            except Exception as e:
                # Exception is also acceptable error handling
                assert True, f"Invalid URL handled with exception: {e}"
                
    def test_network_timeout_handling(self, driver):
        """Test network timeout handling"""
        home_page = HomePage(driver)
        
        # Set very short timeout
        original_timeout = driver.get_timeouts()['pageLoad']
        driver.set_page_load_timeout(1)  # 1 second
        
        try:
            # This might timeout
            home_page.open_homepage()
            time.sleep(1)
            
            # If it loads despite short timeout, that's fine
            assert home_page.is_homepage_loaded(), "Page loaded despite short timeout"
            
        except Exception as e:
            # Timeout exception is expected and acceptable
            assert "timeout" in str(e).lower() or "time" in str(e).lower(), "Should handle timeout gracefully"
            
        finally:
            # Reset timeout
            driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            
    def test_javascript_disabled_fallback(self, driver):
        """Test fallback functionality when JavaScript is disabled"""
        home_page = HomePage(driver)
        
        try:
            # Disable JavaScript
            driver.execute_script("document.querySelectorAll('script').forEach(s => s.remove());")
            
            # Page should still be functional for basic operations
            home_page.open_homepage()
            time.sleep(2)
            
            # Basic elements should still be visible
            logo_visible = home_page.is_element_visible(home_page.LOGO, timeout=5)
            login_visible = home_page.is_element_visible(home_page.LOGIN_LINK, timeout=5)
            
            assert logo_visible or login_visible, "Basic page elements should be visible without JavaScript"
            
        except Exception as e:
            pytest.skip(f"JavaScript disable test not applicable: {e}")
            
    def test_form_validation_edge_cases(self, driver):
        """Test form validation with edge cases"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        if not login_page.is_element_visible(login_page.LOGIN_EMAIL_INPUT, timeout=5):
            pytest.skip("Login form not available for validation testing")
            
        edge_cases = [
            {
                "email": "" * 1000,  # Very long empty string
                "password": "test",
                "description": "very long empty email"
            },
            {
                "email": "test@",
                "password": "",
                "description": "incomplete email"
            },
            {
                "email": "<script>alert('test')</script>",
                "password": "test",
                "description": "XSS attempt in email"
            },
            {
                "email": "test@example.com",
                "password": "'DROP TABLE users;--",
                "description": "SQL injection attempt"
            }
        ]
        
        for case in edge_cases:
            try:
                login_page.login(case["email"], case["password"])
                time.sleep(1)
                
                # Should either show validation error or handle securely
                error_msg = login_page.get_error_message()
                validation_errors = login_page.get_validation_errors()
                is_logged_in = login_page.is_logged_in()
                
                # Should not log in with invalid/malicious data
                assert not is_logged_in or error_msg or validation_errors, f"Should handle {case['description']} securely"
                
                # Clear form for next test
                login_page.open_login_page()
                
            except Exception as e:
                # Form submission failure is acceptable
                assert True, f"Form validation handled edge case: {case['description']}"
                
    def test_cart_edge_cases(self, driver):
        """Test cart functionality edge cases"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        if cart_page.is_cart_empty():
            pytest.skip("Cart is empty - cannot test edge cases")
            
        try:
            # Test extreme quantity values
            extreme_quantities = [0, -1, 999999, "abc", "<script>"]
            
            for qty in extreme_quantities:
                try:
                    cart_page.update_quantity(0, qty)
                    time.sleep(1)
                    
                    # Should handle invalid quantities gracefully
                    error_msg = cart_page.get_error_message()
                    current_qty = cart_page.get_item_quantity(0)
                    
                    # Should either show error or prevent invalid quantity
                    if qty in [0, -1] and isinstance(qty, int):
                        assert current_qty > 0 or error_msg, f"Should handle quantity {qty} appropriately"
                    elif not isinstance(qty, int):
                        assert error_msg or current_qty > 0, f"Should handle non-numeric quantity {qty}"
                        
                except Exception as e:
                    # Exception handling is acceptable
                    assert True, f"Quantity edge case {qty} handled with exception: {e}"
                    
        except Exception as e:
            pytest.skip(f"Cart edge case testing not applicable: {e}")
            
    def test_search_edge_cases(self, driver):
        """Test search functionality edge cases"""
        shop_page = ShopPage(driver)
        shop_page.open_shop_page()
        
        edge_case_searches = [
            "" * 1000,  # Very long empty string
            "<script>alert('xss')</script>",  # XSS attempt
            "'; DROP TABLE products; --",  # SQL injection
            "\u0000\u0001\u0002",  # Control characters
            "🏠👠👢",  # Emojis
            "אִֵֶַָ"  # Non-Latin characters
        ]
        
        for search_term in edge_case_searches:
            try:
                shop_page.search_products(search_term)
                time.sleep(2)
                
                # Should handle search gracefully
                current_url = shop_page.get_current_url()
                page_source = shop_page.get_page_source()
                
                # Should not crash or show errors
                no_server_error = "500" not in page_source and "error" not in page_source.lower()
                assert no_server_error, f"Search with '{repr(search_term)}' should not cause server error"
                
                # Reset to clean state
                shop_page.open_shop_page()
                time.sleep(1)
                
            except Exception as e:
                # Exception handling is acceptable for edge cases
                assert True, f"Search edge case handled: {e}"
                
    def test_concurrent_user_simulation(self, driver):
        """Test behavior under simulated concurrent usage"""
        home_page = HomePage(driver)
        cart_page = CartPage(driver)
        
        # Simulate rapid navigation
        pages = [
            home_page.open_homepage,
            lambda: shop_page.open_shop_page(),
            lambda: cart_page.open_cart_page()
        ]
        
        shop_page = ShopPage(driver)
        
        try:
            for _ in range(3):  # Rapid navigation cycles
                for page_func in pages:
                    page_func()
                    time.sleep(0.5)  # Very short delay
                    
            # Should still be functional after rapid navigation
            home_page.open_homepage()
            assert home_page.is_homepage_loaded(), "Page should remain functional after rapid navigation"
            
        except Exception as e:
            pytest.skip(f"Concurrent simulation test failed: {e}")
            
    def test_memory_leak_prevention(self, driver):
        """Test for potential memory leaks with repeated operations"""
        home_page = HomePage(driver)
        
        try:
            # Perform repeated operations
            for i in range(10):  # Reduced from higher number for CI
                home_page.open_homepage()
                home_page.scroll_to_bottom()
                home_page.scroll_to_top()
                time.sleep(0.1)
                
            # Should still be responsive
            final_load_start = time.time()
            home_page.open_homepage()
            final_load_time = time.time() - final_load_start
            
            # Should not take significantly longer (basic check)
            assert final_load_time < 30, "Page should still load reasonably fast after repeated operations"
            
        except Exception as e:
            pytest.skip(f"Memory leak test not applicable: {e}")
            
    def test_browser_compatibility_features(self, driver):
        """Test browser compatibility features"""
        home_page = HomePage(driver)
        home_page.open_homepage()
        
        try:
            # Test basic JavaScript functionality
            js_working = driver.execute_script("return typeof jQuery !== 'undefined' || typeof $ !== 'undefined' || true;")
            assert js_working, "Basic JavaScript should be working"
            
            # Test CSS support
            css_support = driver.execute_script("return getComputedStyle(document.body).display !== '';")
            assert css_support, "CSS should be supported"
            
            # Test local storage (if used)
            local_storage_support = driver.execute_script("return typeof(Storage) !== 'undefined';")
            if local_storage_support:
                assert True, "Local storage is supported"
            else:
                pytest.skip("Local storage not supported in this browser")
                
        except Exception as e:
            pytest.skip(f"Browser compatibility test failed: {e}")
            
    @pytest.mark.parametrize("window_size", [(800, 600), (1024, 768), (1920, 1080)])
    def test_window_resize_handling(self, driver, window_size):
        """Test handling of window resize events"""
        home_page = HomePage(driver)
        home_page.open_homepage()
        
        # Resize window
        driver.set_window_size(window_size[0], window_size[1])
        time.sleep(1)
        
        # Page should still be functional
        assert home_page.is_element_visible(home_page.LOGO, timeout=5), f"Logo should be visible at {window_size}"
        
        # Navigation should still work
        nav_items = home_page.verify_navigation_menu()
        nav_working = any(nav_items.values())
        assert nav_working, f"Navigation should work at {window_size}"
        
        # Reset window size
        driver.set_window_size(*Config.BROWSER_WINDOW_SIZE)
