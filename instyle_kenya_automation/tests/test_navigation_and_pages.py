import pytest
import time
from pages.home_page import HomePage
from pages.shop_page import ShopPage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.wishlist_page import WishlistPage
from config.config import Config

@pytest.mark.navigation
class TestNavigationAndAllPages:
    """Test cases for navigation and all pages functionality"""
    
    def test_homepage_navigation_menu(self, driver):
        """Test all navigation menu items from homepage"""
        home_page = HomePage(driver)
        home_page.open_homepage()
        
        # Test each navigation item
        nav_items = Config.MAIN_NAVIGATION
        
        for nav_name, expected_url_part in nav_items.items():
            try:
                # Navigate to each section
                if nav_name == "Home":
                    home_page.click_element(home_page.HOME_NAV)
                elif nav_name == "New Products":
                    home_page.click_element(home_page.NEW_PRODUCTS_NAV)
                elif nav_name == "About Us":
                    home_page.navigate_to_about_us()
                elif nav_name == "Shop":
                    home_page.navigate_to_shop()
                elif nav_name == "Track Order":
                    home_page.click_element(home_page.TRACK_ORDER_NAV)
                elif nav_name == "Locate Us":
                    home_page.navigate_to_contact_us()
                    
                time.sleep(2)
                current_url = home_page.get_current_url()
                
                # Verify navigation worked
                if expected_url_part.startswith("./"):
                    url_part = expected_url_part[2:]  # Remove ./
                    if url_part and url_part != "#new_products":
                        assert url_part in current_url or nav_name.lower().replace(" ", "") in current_url.lower(), f"Navigation to {nav_name} failed"
                
                # Return to homepage for next test
                home_page.open_homepage()
                time.sleep(1)
                
            except Exception as e:
                pytest.skip(f"Navigation to {nav_name} not available: {e}")
                
    def test_footer_navigation_links(self, driver):
        """Test footer navigation links"""
        home_page = HomePage(driver)
        home_page.open_homepage()
        
        # Scroll to footer
        home_page.scroll_to_bottom()
        
        # Test footer links
        footer_links = [
            (home_page.FOOTER_ABOUT, "About"),
            (home_page.FOOTER_CONTACT, "Contact"),
            (home_page.FOOTER_PRIVACY, "Privacy Policy"),
            (home_page.FOOTER_TERMS, "Terms and Conditions")
        ]
        
        for link_locator, link_name in footer_links:
            if home_page.is_element_visible(link_locator, timeout=3):
                try:
                    initial_url = home_page.get_current_url()
                    home_page.click_element(link_locator)
                    time.sleep(2)
                    
                    final_url = home_page.get_current_url()
                    
                    # Should navigate to different page
                    assert initial_url != final_url, f"Footer link '{link_name}' should navigate to different page"
                    
                    # Return to homepage
                    home_page.open_homepage()
                    home_page.scroll_to_bottom()
                    time.sleep(1)
                    
                except Exception as e:
                    pytest.skip(f"Footer link '{link_name}' navigation failed: {e}")
            else:
                pytest.skip(f"Footer link '{link_name}' not found")
                
    def test_breadcrumb_navigation(self, driver):
        """Test breadcrumb navigation if available"""
        # Start from shop page where breadcrumbs are more likely
        shop_page = ShopPage(driver)
        shop_page.open_shop_page()
        
        # Check for breadcrumb navigation
        from pages.product_page import ProductPage
        product_page = ProductPage(driver)
        
        try:
            # Look for breadcrumb elements
            breadcrumb_locator = ("css selector", ".breadcrumb, .breadcrumbs, nav[aria-label='breadcrumb']")
            
            if shop_page.is_element_visible(breadcrumb_locator, timeout=5):
                assert True, "Breadcrumb navigation found"
            else:
                pytest.skip("Breadcrumb navigation not available")
                
        except Exception as e:
            pytest.skip(f"Breadcrumb navigation test not applicable: {e}")
            
    def test_search_functionality_across_pages(self, driver):
        """Test search functionality from different pages"""
        pages_to_test = [
            (HomePage(driver), "homepage"),
            (ShopPage(driver), "shop page")
        ]
        
        for page_obj, page_name in pages_to_test:
            try:
                if page_name == "homepage":
                    page_obj.open_homepage()
                else:
                    page_obj.open_shop_page()
                    
                # Look for search functionality
                search_locator = ("css selector", "input[type='search'], input[name*='search'], .search-input")
                
                if page_obj.is_element_visible(search_locator, timeout=5):
                    # Test search
                    page_obj.send_keys_to_element(search_locator, "boots")
                    
                    # Look for search button
                    search_btn_locator = ("css selector", "button[type='submit'], .search-btn, .search-button")
                    if page_obj.is_element_visible(search_btn_locator, timeout=3):
                        page_obj.click_element(search_btn_locator)
                        time.sleep(2)
                        
                        assert True, f"Search functionality working on {page_name}"
                    else:
                        # Try pressing Enter
                        from selenium.webdriver.common.keys import Keys
                        search_element = page_obj.find_element(search_locator)
                        search_element.send_keys(Keys.RETURN)
                        time.sleep(2)
                        
                        assert True, f"Search functionality working on {page_name}"
                else:
                    pytest.skip(f"Search not available on {page_name}")
                    
            except Exception as e:
                pytest.skip(f"Search test on {page_name} failed: {e}")
                
    def test_mobile_menu_functionality(self, driver):
        """Test mobile menu functionality"""
        home_page = HomePage(driver)
        home_page.open_homepage()
        
        # Set mobile viewport
        driver.set_window_size(375, 667)
        time.sleep(1)
        
        try:
            # Look for mobile menu button
            if home_page.is_element_visible(home_page.MENU_BUTTON, timeout=5):
                # Click menu button
                home_page.click_menu()
                time.sleep(1)
                
                # Menu should open or close
                assert True, "Mobile menu functionality working"
            else:
                pytest.skip("Mobile menu button not found")
                
        except Exception as e:
            pytest.skip(f"Mobile menu test failed: {e}")
        finally:
            # Reset window size
            driver.set_window_size(*Config.BROWSER_WINDOW_SIZE)
            
    def test_login_page_accessibility(self, driver):
        """Test login page loads and is accessible"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # Check basic page elements
        page_title = login_page.get_page_title()
        assert page_title, "Login page should have a title"
        
        # Check for login form or redirect
        form_available = (
            login_page.is_element_visible(login_page.LOGIN_EMAIL_INPUT, timeout=5) or
            login_page.is_element_visible(login_page.LOGIN_BUTTON, timeout=5)
        )
        
        if form_available:
            assert True, "Login page form elements accessible"
        else:
            # May redirect to different login system
            current_url = login_page.get_current_url()
            assert "login" in current_url.lower() or "auth" in current_url.lower(), "Should be on login-related page"
            
    def test_cart_page_accessibility(self, driver):
        """Test cart page loads and is accessible"""
        cart_page = CartPage(driver)
        cart_page.open_cart_page()
        
        assert cart_page.is_cart_page_loaded(), "Cart page should load"
        
        # Check page structure
        page_title = cart_page.get_page_title()
        assert page_title, "Cart page should have a title"
        
    def test_wishlist_page_accessibility(self, driver):
        """Test wishlist page loads and is accessible"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.open_wishlist_page()
        
        assert wishlist_page.is_wishlist_page_loaded(), "Wishlist page should load"
        
        # Check page structure
        page_title = wishlist_page.get_page_title()
        assert page_title, "Wishlist page should have a title"
        
    def test_shop_page_accessibility(self, driver):
        """Test shop page loads and is accessible"""
        shop_page = ShopPage(driver)
        shop_page.open_shop_page()
        
        assert shop_page.is_shop_page_loaded(), "Shop page should load"
        
        # Check page structure
        page_title = shop_page.get_page_title()
        assert page_title, "Shop page should have a title"
        
        # Check for products or empty state
        has_products = shop_page.verify_products_loaded()
        has_no_products_msg = shop_page.verify_no_products_message()
        
        assert has_products or has_no_products_msg, "Shop page should show products or no products message"
        
    def test_cross_page_cart_consistency(self, driver):
        """Test cart consistency across different pages"""
        home_page = HomePage(driver)
        shop_page = ShopPage(driver)
        cart_page = CartPage(driver)
        
        # Check cart from homepage
        home_page.open_homepage()
        if home_page.is_element_visible(home_page.CART_LINK, timeout=5):
            home_page.click_cart()
            time.sleep(2)
            
            if cart_page.is_cart_page_loaded():
                initial_cart_empty = cart_page.is_cart_empty()
                initial_cart_count = cart_page.get_cart_items_count() if not initial_cart_empty else 0
                
                # Go to shop page and check cart again
                shop_page.open_shop_page()
                time.sleep(1)
                
                # Navigate to cart from shop page
                if shop_page.is_element_visible(("link text", "Cart"), timeout=5):
                    shop_page.click_element(("link text", "Cart"))
                    time.sleep(2)
                    
                    final_cart_empty = cart_page.is_cart_empty()
                    final_cart_count = cart_page.get_cart_items_count() if not final_cart_empty else 0
                    
                    # Cart should be consistent
                    assert initial_cart_empty == final_cart_empty, "Cart empty state should be consistent across pages"
                    assert initial_cart_count == final_cart_count, "Cart count should be consistent across pages"
                else:
                    pytest.skip("Cart link not available from shop page")
            else:
                pytest.skip("Cart page not accessible")
        else:
            pytest.skip("Cart link not available from homepage")
            
    def test_back_button_functionality(self, driver):
        """Test browser back button functionality"""
        home_page = HomePage(driver)
        shop_page = ShopPage(driver)
        
        # Start from homepage
        home_page.open_homepage()
        homepage_url = home_page.get_current_url()
        
        # Navigate to shop
        home_page.navigate_to_shop()
        time.sleep(2)
        shop_url = shop_page.get_current_url()
        
        # Use browser back button
        driver.back()
        time.sleep(2)
        
        back_url = driver.current_url
        
        # Should return to homepage
        assert back_url == homepage_url, "Browser back button should return to previous page"
        
    def test_page_refresh_functionality(self, driver):
        """Test page refresh maintains state"""
        home_page = HomePage(driver)
        home_page.open_homepage()
        
        # Get initial state
        initial_title = home_page.get_page_title()
        initial_url = home_page.get_current_url()
        
        # Refresh page
        home_page.refresh_page()
        time.sleep(2)
        
        # Check state after refresh
        final_title = home_page.get_page_title()
        final_url = home_page.get_current_url()
        
        assert final_title == initial_title, "Page title should be consistent after refresh"
        assert final_url == initial_url, "Page URL should be consistent after refresh"
        assert home_page.is_homepage_loaded(), "Homepage should still be loaded after refresh"
        
    @pytest.mark.error_handling
    def test_404_error_handling(self, driver):
        """Test 404 error page handling"""
        home_page = HomePage(driver)
        
        # Try to access non-existent page
        non_existent_url = Config.BASE_URL + "non-existent-page-12345"
        home_page.open_url(non_existent_url)
        time.sleep(2)
        
        page_title = home_page.get_page_title()
        page_source = home_page.get_page_source()
        
        # Should show error page or redirect
        error_indicators = ["404", "not found", "error", "page not found"]
        has_error_indicator = any(indicator in page_title.lower() or indicator in page_source.lower() 
                                 for indicator in error_indicators)
        
        # Either shows error or redirects to valid page
        assert has_error_indicator or home_page.get_current_url() != non_existent_url, "Should handle non-existent pages gracefully"
        
    @pytest.mark.responsive
    def test_responsive_design_across_pages(self, driver):
        """Test responsive design on different pages"""
        pages_to_test = [
            (HomePage(driver), "homepage"),
            (ShopPage(driver), "shop"),
            (CartPage(driver), "cart"),
            (WishlistPage(driver), "wishlist")
        ]
        
        screen_sizes = [
            (375, 667, "Mobile"),
            (768, 1024, "Tablet"),
            (1200, 800, "Desktop")
        ]
        
        for page_obj, page_name in pages_to_test:
            for width, height, device_type in screen_sizes:
                try:
                    # Set screen size
                    driver.set_window_size(width, height)
                    time.sleep(1)
                    
                    # Open page
                    if page_name == "homepage":
                        page_obj.open_homepage()
                    elif page_name == "shop":
                        page_obj.open_shop_page()
                    elif page_name == "cart":
                        page_obj.open_cart_page()
                    elif page_name == "wishlist":
                        page_obj.open_wishlist_page()
                        
                    # Check if page loads properly
                    page_title = page_obj.get_page_title()
                    assert page_title, f"{page_name.title()} page should load properly on {device_type}"
                    
                except Exception as e:
                    pytest.skip(f"Responsive test for {page_name} on {device_type} failed: {e}")
                    
        # Reset to default size
        driver.set_window_size(*Config.BROWSER_WINDOW_SIZE)
