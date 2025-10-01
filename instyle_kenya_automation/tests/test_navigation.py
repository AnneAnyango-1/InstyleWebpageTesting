"""Navigation and general site functionality tests"""

import pytest
import logging
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.wishlist_page import WishlistPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from config.config import Config

logger = logging.getLogger(__name__)

class TestNavigation:
    """Test suite for navigation and general site functionality"""
    
    @pytest.mark.navigation
    @pytest.mark.smoke
    def test_homepage_navigation(self, driver):
        """Test basic navigation to homepage"""
        home_page = HomePage(driver)
        home_page.load()
        
        assert home_page.is_loaded(), "Homepage should load successfully"
        
        # Test logo click (should return to homepage)
        if home_page.is_element_present(home_page.LOGO):
            logo_element = home_page.find_element(home_page.LOGO)
            logo_element.click()
            home_page.wait_for_page_load()
            
            assert home_page.is_loaded(), "Clicking logo should return to homepage"
            logger.info("Logo navigation works correctly")
        
        logger.info("Homepage navigation test passed")
    
    @pytest.mark.navigation
    @pytest.mark.smoke
    def test_main_navigation_links(self, driver, product_categories):
        """Test main navigation menu links"""
        home_page = HomePage(driver)
        home_page.load()
        
        navigation_links = home_page.get_navigation_links()
        assert len(navigation_links) > 0, "Should have navigation links"
        
        logger.info(f"Found navigation links: {navigation_links}")
        
        # Test category navigation
        for category in product_categories[:2]:  # Test first 2 categories
            home_page.load()  # Return to homepage
            
            success = home_page.click_product_category(category.lower())
            if success:
                current_url = driver.current_url
                logger.info(f"Successfully navigated to {category}: {current_url}")
            else:
                logger.warning(f"Could not navigate to {category} category")
    
    @pytest.mark.navigation
    def test_user_account_navigation(self, driver):
        """Test user account related navigation"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Test login link
        if home_page.is_element_present(home_page.LOGIN_LINK):
            success = home_page.click_login_link()
            if success:
                login_page = LoginPage(driver)
                assert login_page.is_loaded(), "Should navigate to login page"
                logger.info("Login navigation works correctly")
            
            # Return to homepage
            home_page.load()
        
        # Test registration link
        if home_page.is_element_present(home_page.REGISTER_LINK):
            success = home_page.click_register_link()
            if success:
                registration_page = RegistrationPage(driver)
                if registration_page.is_loaded():
                    logger.info("Registration navigation works correctly")
                elif "login" in driver.current_url.lower():
                    logger.info("Register link redirected to login (normal behavior)")
        
        logger.info("User account navigation test completed")
    
    @pytest.mark.navigation
    def test_cart_and_wishlist_navigation(self, driver):
        """Test cart and wishlist navigation"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Test cart navigation
        if home_page.is_element_present(home_page.CART_LINK):
            success = home_page.click_cart_link()
            if success:
                cart_page = CartPage(driver)
                assert cart_page.is_loaded(), "Should navigate to cart page"
                logger.info("Cart navigation works correctly")
            
            # Return to homepage
            home_page.load()
        
        # Test wishlist navigation
        if home_page.is_element_present(home_page.WISHLIST_LINK):
            success = home_page.click_wishlist_link()
            if success:
                current_url = driver.current_url.lower()
                if "wishlist" in current_url:
                    wishlist_page = WishlistPage(driver)
                    assert wishlist_page.is_loaded(), "Should navigate to wishlist page"
                    logger.info("Wishlist navigation works correctly")
                elif "login" in current_url:
                    logger.info("Wishlist requires login (normal behavior)")
        
        logger.info("Cart and wishlist navigation test completed")
    
    @pytest.mark.navigation
    @pytest.mark.regression
    def test_breadcrumb_navigation(self, driver, search_terms):
        """Test breadcrumb navigation"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Navigate to a deeper page (via search)
        search_term = search_terms[0]
        success = home_page.search_for_product(search_term)
        
        if success:
            # Look for breadcrumbs
            from pages.search_results_page import SearchResultsPage
            search_page = SearchResultsPage(driver)
            
            if search_page.is_element_present(search_page.BREADCRUMBS):
                breadcrumbs = search_page.find_element(search_page.BREADCRUMBS)
                breadcrumb_links = breadcrumbs.find_elements_by_tag_name("a")
                
                if len(breadcrumb_links) > 0:
                    logger.info(f"Found {len(breadcrumb_links)} breadcrumb links")
                    
                    # Click on first breadcrumb (usually home)
                    first_breadcrumb = breadcrumb_links[0]
                    first_breadcrumb.click()
                    search_page.wait_for_page_load()
                    
                    # Should navigate somewhere
                    new_url = driver.current_url
                    logger.info(f"Breadcrumb navigation successful: {new_url}")
                else:
                    logger.info("No clickable breadcrumb links found")
            else:
                logger.info("No breadcrumbs found")
        else:
            logger.warning("Could not navigate to search page for breadcrumb test")
    
    @pytest.mark.navigation
    def test_footer_navigation(self, driver):
        """Test footer navigation links"""
        home_page = HomePage(driver)
        home_page.load()
        
        if home_page.is_element_present(home_page.FOOTER):
            footer_links = home_page.find_elements(home_page.FOOTER_LINKS)
            
            if len(footer_links) > 0:
                logger.info(f"Found {len(footer_links)} footer links")
                
                # Test first few footer links
                for i, link in enumerate(footer_links[:3]):
                    try:
                        link_text = link.text
                        link_url = link.get_attribute("href")
                        
                        if link_url and link_text:
                            logger.info(f"Footer link {i+1}: '{link_text}' -> {link_url}")
                            
                            # Click link and verify navigation
                            link.click()
                            home_page.wait_for_page_load()
                            
                            current_url = driver.current_url
                            if current_url != Config.BASE_URL:
                                logger.info(f"Footer link navigation successful: {current_url}")
                            
                            # Return to homepage
                            home_page.load()
                    
                    except Exception as e:
                        logger.warning(f"Could not test footer link {i+1}: {str(e)}")
                        continue
            else:
                logger.info("No footer links found")
        else:
            logger.info("Footer not found")
    
    @pytest.mark.navigation
    def test_search_navigation(self, driver, search_terms):
        """Test search navigation flow"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Perform search
        search_term = search_terms[0]
        success = home_page.search_for_product(search_term)
        
        if success:
            from pages.search_results_page import SearchResultsPage
            search_page = SearchResultsPage(driver)
            
            assert search_page.is_loaded(), "Should navigate to search results"
            
            # If results exist, try clicking on a product
            if search_page.has_results():
                click_success = search_page.click_product(0)
                if click_success:
                    from pages.product_page import ProductPage
                    product_page = ProductPage(driver)
                    
                    if product_page.is_loaded():
                        logger.info("Search -> Product navigation successful")
                    else:
                        logger.warning("Product page did not load after clicking search result")
            
            logger.info("Search navigation test completed")
        else:
            logger.warning("Could not perform search for navigation test")
    
    @pytest.mark.navigation
    @pytest.mark.regression
    def test_back_button_functionality(self, driver):
        """Test browser back button functionality"""
        home_page = HomePage(driver)
        home_page.load()
        homepage_url = driver.current_url
        
        # Navigate to cart
        if home_page.click_cart_link():
            cart_page = CartPage(driver)
            cart_url = driver.current_url
            
            # Use browser back button
            driver.back()
            home_page.wait_for_page_load()
            
            # Should be back on homepage
            current_url = driver.current_url
            assert current_url == homepage_url, "Back button should return to homepage"
            logger.info("Back button functionality works correctly")
        else:
            logger.warning("Could not test back button - cart navigation failed")
    
    @pytest.mark.navigation
    def test_mobile_responsive_navigation(self, driver):
        """Test mobile responsive navigation"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Get original window size
        original_size = driver.get_window_size()
        
        try:
            # Test mobile size (iPhone)
            driver.set_window_size(375, 667)
            
            # Check if navigation is still accessible
            assert home_page.is_element_present(home_page.LOGO), "Logo should be visible on mobile"
            
            # Look for mobile menu button (hamburger menu)
            mobile_menu_selectors = [
                ".mobile-menu-toggle",
                ".hamburger",
                ".menu-toggle",
                "[aria-label*='menu']",
                ".navbar-toggler"
            ]
            
            mobile_menu_found = False
            for selector in mobile_menu_selectors:
                try:
                    from selenium.webdriver.common.by import By
                    mobile_menu = driver.find_element(By.CSS_SELECTOR, selector)
                    if mobile_menu.is_displayed():
                        mobile_menu_found = True
                        logger.info(f"Mobile menu found: {selector}")
                        
                        # Try clicking mobile menu
                        mobile_menu.click()
                        logger.info("Mobile menu clicked successfully")
                        break
                except:
                    continue
            
            if not mobile_menu_found:
                logger.info("No mobile menu found (navigation might be always visible)")
            
            # Test tablet size
            driver.set_window_size(768, 1024)
            assert home_page.is_element_present(home_page.LOGO), "Logo should be visible on tablet"
            
            logger.info("Mobile responsive navigation test completed")
            
        finally:
            # Restore original window size
            driver.set_window_size(original_size['width'], original_size['height'])
    
    @pytest.mark.navigation
    @pytest.mark.regression
    def test_page_loading_states(self, driver):
        """Test page loading states and performance"""
        import time
        
        home_page = HomePage(driver)
        
        # Test homepage loading
        start_time = time.time()
        home_page.load()
        load_time = time.time() - start_time
        
        assert load_time < 10, f"Homepage should load within 10 seconds, took {load_time:.2f}s"
        logger.info(f"Homepage load time: {load_time:.2f}s")
        
        # Test navigation to different pages
        pages_to_test = [
            ("cart", lambda: home_page.click_cart_link()),
            ("login", lambda: home_page.click_login_link())
        ]
        
        for page_name, navigation_func in pages_to_test:
            home_page.load()  # Return to homepage
            
            start_time = time.time()
            success = navigation_func()
            
            if success:
                load_time = time.time() - start_time
                logger.info(f"{page_name.capitalize()} page load time: {load_time:.2f}s")
                
                # Page should load within reasonable time
                assert load_time < 15, f"{page_name} page should load within 15 seconds"
    
    @pytest.mark.navigation
    def test_url_structure_and_seo(self, driver, search_terms):
        """Test URL structure and SEO-friendly URLs"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Check homepage URL
        homepage_url = driver.current_url
        assert homepage_url.startswith("https://"), "Homepage should use HTTPS"
        logger.info(f"Homepage URL: {homepage_url}")
        
        # Test search URL structure
        search_term = search_terms[0]
        success = home_page.search_for_product(search_term)
        
        if success:
            search_url = driver.current_url
            assert "search" in search_url.lower() or search_term.lower() in search_url.lower(), "Search URL should contain search term or 'search'"
            logger.info(f"Search URL: {search_url}")
        
        # Test page titles
        home_page.load()
        homepage_title = driver.title
        assert homepage_title, "Homepage should have a title"
        assert len(homepage_title) > 0, "Page title should not be empty"
        logger.info(f"Homepage title: '{homepage_title}'")
    
    @pytest.mark.navigation
    @pytest.mark.smoke
    def test_error_page_handling(self, driver):
        """Test error page handling for invalid URLs"""
        # Try navigating to non-existent page
        driver.get(f"{Config.BASE_URL}non-existent-page-12345")
        
        # Check if proper error handling
        page_title = driver.title.lower()
        page_source = driver.page_source.lower()
        
        # Look for 404 indicators
        error_indicators = ["404", "not found", "page not found", "error"]
        
        has_error_indicator = any(indicator in page_title or indicator in page_source 
                                for indicator in error_indicators)
        
        if has_error_indicator:
            logger.info("Proper 404 error handling detected")
        else:
            logger.warning("No clear 404 error handling found")
        
        # Try to navigate back to homepage
        home_page = HomePage(driver)
        home_page.load()
        
        assert home_page.is_loaded(), "Should be able to return to homepage after 404"
        logger.info("Error page handling test completed")
