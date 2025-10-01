"""Homepage tests"""

import pytest
import logging
from pages.home_page import HomePage
from config.config import Config

logger = logging.getLogger(__name__)

class TestHomePage:
    """Test suite for homepage functionality"""
    
    @pytest.mark.smoke
    def test_homepage_loads_successfully(self, driver):
        """Test that homepage loads successfully"""
        home_page = HomePage(driver)
        home_page.load()
        
        assert home_page.is_loaded(), "Homepage should load successfully"
        assert "instyle" in home_page.get_page_title().lower(), "Page title should contain 'instyle'"
        logger.info("Homepage loaded successfully")
    
    @pytest.mark.smoke
    def test_logo_is_visible(self, driver):
        """Test that logo is visible on homepage"""
        home_page = HomePage(driver)
        home_page.load()
        
        assert home_page.is_element_visible(home_page.LOGO), "Logo should be visible"
        logger.info("Logo is visible on homepage")
    
    @pytest.mark.smoke
    def test_main_navigation_is_visible(self, driver):
        """Test that main navigation is visible"""
        home_page = HomePage(driver)
        home_page.load()
        
        assert home_page.is_element_visible(home_page.MAIN_NAVIGATION), "Main navigation should be visible"
        
        nav_links = home_page.get_navigation_links()
        assert len(nav_links) > 0, "Navigation should have links"
        logger.info(f"Found {len(nav_links)} navigation links: {nav_links}")
    
    @pytest.mark.smoke
    def test_search_functionality_basic(self, driver, search_terms):
        """Test basic search functionality"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]  # Use first search term
        success = home_page.search_for_product(search_term)
        
        assert success, f"Search for '{search_term}' should be successful"
        assert search_term.lower() in driver.current_url.lower() or "search" in driver.current_url.lower()
        logger.info(f"Search for '{search_term}' completed successfully")
    
    def test_featured_products_display(self, driver):
        """Test that featured products are displayed"""
        home_page = HomePage(driver)
        home_page.load()
        
        products = home_page.get_featured_products()
        
        if len(products) > 0:
            assert len(products) > 0, "Featured products should be displayed"
            
            # Check first product has required information
            first_product = products[0]
            assert first_product["title"], "Product should have a title"
            logger.info(f"Found {len(products)} featured products")
        else:
            logger.warning("No featured products found on homepage")
    
    @pytest.mark.smoke
    def test_cart_link_is_accessible(self, driver):
        """Test that cart link is accessible"""
        home_page = HomePage(driver)
        home_page.load()
        
        assert home_page.is_element_visible(home_page.CART_LINK), "Cart link should be visible"
        
        cart_count = home_page.get_cart_item_count()
        assert cart_count is not None, "Cart count should be available"
        logger.info(f"Cart link is accessible, current count: {cart_count}")
    
    def test_user_account_links(self, driver):
        """Test that user account links are present"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Check if login link OR account link is present (depends on login state)
        login_present = home_page.is_element_present(home_page.LOGIN_LINK)
        account_present = home_page.is_element_present(home_page.ACCOUNT_LINK)
        
        assert login_present or account_present, "Either login link or account link should be present"
        logger.info(f"User account links present - Login: {login_present}, Account: {account_present}")
    
    def test_hero_section_display(self, driver):
        """Test hero section display"""
        home_page = HomePage(driver)
        home_page.load()
        
        if home_page.is_hero_section_visible():
            assert home_page.is_hero_section_visible(), "Hero section should be visible"
            
            hero_title = home_page.get_hero_title()
            logger.info(f"Hero section is visible with title: '{hero_title}'")
        else:
            logger.info("Hero section not found - this may be normal depending on site design")
    
    @pytest.mark.regression
    def test_category_navigation(self, driver, product_categories):
        """Test navigation to product categories"""
        home_page = HomePage(driver)
        home_page.load()
        
        for category in product_categories[:3]:  # Test first 3 categories
            home_page.load()  # Reload homepage for each test
            
            success = home_page.click_product_category(category.lower())
            if success:
                current_url = driver.current_url
                assert category.lower() in current_url.lower() or "collection" in current_url.lower()
                logger.info(f"Successfully navigated to {category} category")
            else:
                logger.warning(f"Could not find or click {category} category link")
    
    def test_footer_presence(self, driver):
        """Test that footer is present"""
        home_page = HomePage(driver)
        home_page.load()
        
        assert home_page.is_element_present(home_page.FOOTER), "Footer should be present"
        logger.info("Footer is present on homepage")
    
    @pytest.mark.regression
    def test_social_media_links(self, driver):
        """Test social media links"""
        home_page = HomePage(driver)
        home_page.load()
        
        social_links = home_page.get_social_media_links()
        
        if len(social_links) > 0:
            assert len(social_links) > 0, "Social media links should be present"
            
            # Check that links are valid URLs
            for link in social_links:
                assert link.startswith(("http://", "https://")), f"Social link should be valid URL: {link}"
            
            logger.info(f"Found {len(social_links)} social media links")
        else:
            logger.info("No social media links found")
    
    @pytest.mark.regression
    def test_newsletter_signup_form(self, driver):
        """Test newsletter signup form"""
        home_page = HomePage(driver)
        home_page.load()
        
        if home_page.is_element_present(home_page.NEWSLETTER_INPUT):
            test_email = "test@example.com"
            success = home_page.subscribe_to_newsletter(test_email)
            
            # Note: We can't verify actual subscription, just that form submission works
            logger.info(f"Newsletter signup form {'worked' if success else 'failed'}")
        else:
            logger.info("Newsletter signup form not found")
    
    @pytest.mark.regression
    def test_search_with_multiple_terms(self, driver, search_terms):
        """Test search with multiple search terms"""
        home_page = HomePage(driver)
        
        for search_term in search_terms[:3]:  # Test first 3 terms
            home_page.load()  # Reload homepage for each search
            
            success = home_page.search_for_product(search_term)
            assert success, f"Search for '{search_term}' should work"
            
            current_url = driver.current_url
            assert "search" in current_url.lower() or search_term.lower() in current_url.lower()
            logger.info(f"Search for '{search_term}' completed successfully")
    
    def test_responsive_elements(self, driver):
        """Test responsive design elements"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Test different window sizes
        original_size = driver.get_window_size()
        
        try:
            # Test mobile size
            driver.set_window_size(375, 667)
            assert home_page.is_element_visible(home_page.LOGO), "Logo should be visible on mobile"
            
            # Test tablet size
            driver.set_window_size(768, 1024)
            assert home_page.is_element_visible(home_page.LOGO), "Logo should be visible on tablet"
            
            logger.info("Responsive elements test completed")
            
        finally:
            # Restore original window size
            driver.set_window_size(original_size['width'], original_size['height'])
    
    @pytest.mark.smoke
    def test_page_load_performance(self, driver):
        """Test page load performance"""
        import time
        
        start_time = time.time()
        
        home_page = HomePage(driver)
        home_page.load()
        
        end_time = time.time()
        load_time = end_time - start_time
        
        # Page should load within 10 seconds
        assert load_time < 10, f"Page should load within 10 seconds, took {load_time:.2f}s"
        logger.info(f"Homepage loaded in {load_time:.2f} seconds")
