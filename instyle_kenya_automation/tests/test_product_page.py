"""Product page functionality tests"""

import pytest
import logging
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.search_results_page import SearchResultsPage
from config.config import Config

logger = logging.getLogger(__name__)

class TestProductPage:
    """Test suite for product page functionality"""
    
    def get_product_page(self, driver, search_terms):
        """Helper method to navigate to a product page"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Search for a product
        search_term = search_terms[0]
        success = home_page.search_for_product(search_term)
        
        if success:
            search_page = SearchResultsPage(driver)
            if search_page.has_results():
                # Click on first product
                if search_page.click_product(0):
                    product_page = ProductPage(driver)
                    if product_page.is_loaded():
                        return product_page
        
        return None
    
    @pytest.mark.product
    @pytest.mark.smoke
    def test_product_page_loads(self, driver, search_terms):
        """Test that product page loads successfully"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            assert product_page.is_loaded(), "Product page should load successfully"
            logger.info("Product page loaded successfully")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    @pytest.mark.smoke
    def test_product_information_display(self, driver, search_terms):
        """Test that product information is displayed correctly"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            # Check product title
            title = product_page.get_product_title()
            assert title, "Product should have a title"
            
            # Check product price
            price = product_page.get_product_price()
            assert price, "Product should have a price"
            
            # Check product description
            description = product_page.get_product_description()
            # Description might be in a tab or not visible initially
            
            logger.info(f"Product info - Title: '{title}', Price: '{price}'")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_product_images(self, driver, search_terms):
        """Test product image display and thumbnail functionality"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            # Check main product image
            assert product_page.is_element_present(product_page.MAIN_PRODUCT_IMAGE), "Main product image should be present"
            
            # Check thumbnail images if present
            if product_page.is_element_present(product_page.THUMBNAIL_IMAGES):
                thumbnails = product_page.find_elements(product_page.THUMBNAIL_IMAGES)
                if len(thumbnails) > 1:
                    # Try clicking on second thumbnail
                    success = product_page.click_thumbnail_image(1)
                    if success:
                        logger.info("Successfully clicked on thumbnail image")
                    else:
                        logger.warning("Could not click on thumbnail image")
                else:
                    logger.info("Only one product image available")
            else:
                logger.info("No thumbnail images found")
            
            logger.info("Product images test completed")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    @pytest.mark.smoke
    def test_add_to_cart_functionality(self, driver, search_terms):
        """Test add to cart functionality"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            # Check if product is in stock
            if product_page.is_in_stock():
                # Try to add to cart
                success = product_page.add_to_cart()
                
                if success:
                    # Check for success message
                    success_msg = product_page.get_success_message()
                    if success_msg:
                        logger.info(f"Add to cart successful with message: '{success_msg}'")
                    else:
                        logger.info("Add to cart appears successful")
                else:
                    logger.warning("Could not add product to cart")
            else:
                logger.info("Product is out of stock, cannot test add to cart")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_quantity_selection(self, driver, search_terms):
        """Test quantity selection functionality"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            if product_page.is_element_present(product_page.QUANTITY_INPUT):
                # Test setting quantity
                success = product_page.set_quantity(3)
                if success:
                    # Verify quantity was set
                    quantity_value = product_page.get_element_attribute(product_page.QUANTITY_INPUT, "value")
                    assert quantity_value == "3", "Quantity should be set to 3"
                    logger.info("Successfully set product quantity to 3")
                
                # Test increase/decrease buttons if present
                if product_page.is_element_present(product_page.QUANTITY_INCREASE):
                    increase_success = product_page.increase_quantity()
                    if increase_success:
                        logger.info("Successfully increased quantity")
                
                if product_page.is_element_present(product_page.QUANTITY_DECREASE):
                    decrease_success = product_page.decrease_quantity()
                    if decrease_success:
                        logger.info("Successfully decreased quantity")
            else:
                logger.info("Quantity input not found")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_product_variants(self, driver, search_terms):
        """Test product variant selection (size, color, etc.)"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            # Test size selection
            if product_page.is_element_present(product_page.SIZE_OPTIONS):
                sizes = ["S", "M", "L", "XL", "Small", "Medium", "Large"]
                for size in sizes:
                    success = product_page.select_size(size)
                    if success:
                        logger.info(f"Successfully selected size: {size}")
                        break
                else:
                    logger.warning("Could not select any size option")
            else:
                logger.info("Size options not available")
            
            # Test color selection
            if product_page.is_element_present(product_page.COLOR_OPTIONS):
                colors = ["Black", "White", "Red", "Blue", "Green"]
                for color in colors:
                    success = product_page.select_color(color)
                    if success:
                        logger.info(f"Successfully selected color: {color}")
                        break
                else:
                    logger.warning("Could not select any color option")
            else:
                logger.info("Color options not available")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_add_to_wishlist(self, driver, search_terms):
        """Test add to wishlist functionality"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            if product_page.is_element_present(product_page.ADD_TO_WISHLIST_BUTTON):
                success = product_page.add_to_wishlist()
                if success:
                    logger.info("Successfully added product to wishlist")
                else:
                    logger.warning("Could not add product to wishlist")
            else:
                logger.info("Add to wishlist button not found")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_product_tabs(self, driver, search_terms):
        """Test product information tabs"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            if product_page.is_element_present(product_page.PRODUCT_TABS):
                # Test different tabs
                tabs = ["description", "specifications", "reviews", "shipping"]
                
                for tab in tabs:
                    success = product_page.switch_to_tab(tab)
                    if success:
                        logger.info(f"Successfully switched to {tab} tab")
                    else:
                        logger.info(f"{tab.capitalize()} tab not available")
            else:
                logger.info("Product tabs not found")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_stock_status_display(self, driver, search_terms):
        """Test stock status display"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            in_stock = product_page.is_in_stock()
            stock_status = product_page.get_stock_status()
            
            logger.info(f"Product stock status - In stock: {in_stock}, Status text: '{stock_status}'")
            
            # Add to cart button should be enabled if in stock
            if in_stock:
                add_to_cart_button = product_page.find_element(product_page.ADD_TO_CART_BUTTON)
                assert add_to_cart_button.is_enabled(), "Add to cart button should be enabled for in-stock products"
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    @pytest.mark.regression
    def test_product_reviews(self, driver, search_terms):
        """Test product reviews section"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            # Switch to reviews tab if it exists
            product_page.switch_to_tab("reviews")
            
            if product_page.is_element_present(product_page.REVIEWS_SECTION):
                reviews = product_page.get_reviews()
                
                if len(reviews) > 0:
                    logger.info(f"Found {len(reviews)} reviews")
                    
                    # Check first review
                    first_review = reviews[0]
                    assert first_review["text"], "Review should have text"
                    logger.info(f"First review rating: {first_review.get('rating', 'N/A')}")
                else:
                    logger.info("No reviews found for this product")
                
                # Test write review button
                if product_page.is_element_present(product_page.WRITE_REVIEW_BUTTON):
                    # Don't actually click it, just verify it's present
                    logger.info("Write review button is present")
            else:
                logger.info("Reviews section not found")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_related_products(self, driver, search_terms):
        """Test related/recommended products section"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            if product_page.is_element_present(product_page.RELATED_PRODUCTS):
                related_products = product_page.get_related_products()
                
                if len(related_products) > 0:
                    logger.info(f"Found {len(related_products)} related products")
                    
                    # Check first related product
                    first_related = related_products[0]
                    assert first_related["title"], "Related product should have a title"
                    assert first_related["price"], "Related product should have a price"
                    
                    logger.info(f"First related product: {first_related['title']}")
                else:
                    logger.info("No related products found")
            else:
                logger.info("Related products section not found")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_buy_now_functionality(self, driver, search_terms):
        """Test buy now button functionality"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            if product_page.is_element_present(product_page.BUY_NOW_BUTTON):
                if product_page.is_in_stock():
                    # Note: We don't actually complete the purchase
                    # Just verify the button is present and clickable
                    buy_now_button = product_page.find_element(product_page.BUY_NOW_BUTTON)
                    assert buy_now_button.is_enabled(), "Buy now button should be enabled for in-stock products"
                    logger.info("Buy now button is present and enabled")
                else:
                    logger.info("Product is out of stock, buy now not available")
            else:
                logger.info("Buy now button not found")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_share_product(self, driver, search_terms):
        """Test share product functionality"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            if product_page.is_element_present(product_page.SHARE_BUTTON):
                success = product_page.share_product()
                if success:
                    logger.info("Share product button clicked successfully")
                else:
                    logger.warning("Could not click share product button")
            else:
                logger.info("Share product button not found")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_product_sku_display(self, driver, search_terms):
        """Test product SKU display"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            if product_page.is_element_present(product_page.PRODUCT_SKU):
                sku = product_page.get_product_sku()
                assert sku, "Product SKU should be displayed"
                logger.info(f"Product SKU: {sku}")
            else:
                logger.info("Product SKU not displayed")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    @pytest.mark.regression
    def test_product_page_error_handling(self, driver, search_terms):
        """Test product page error handling"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            # Test adding out of stock product to cart
            if not product_page.is_in_stock():
                success = product_page.add_to_cart()
                if not success:
                    error_msg = product_page.get_error_message()
                    logger.info(f"Out of stock product correctly prevented from being added to cart. Error: '{error_msg}'")
                else:
                    logger.warning("Out of stock product was added to cart (unexpected)")
            
            # Test invalid quantity
            if product_page.is_element_present(product_page.QUANTITY_INPUT):
                # Try setting very high quantity
                product_page.set_quantity(999999)
                add_success = product_page.add_to_cart()
                
                if not add_success:
                    error_msg = product_page.get_error_message()
                    logger.info(f"High quantity correctly handled. Error: '{error_msg}'")
        else:
            pytest.skip("Could not navigate to product page")
    
    @pytest.mark.product
    def test_product_page_breadcrumbs(self, driver, search_terms):
        """Test product page breadcrumbs navigation"""
        product_page = self.get_product_page(driver, search_terms)
        
        if product_page:
            if product_page.is_element_present(product_page.BREADCRUMBS):
                breadcrumbs = product_page.find_element(product_page.BREADCRUMBS)
                breadcrumb_links = breadcrumbs.find_elements_by_tag_name("a")
                
                if len(breadcrumb_links) > 0:
                    logger.info(f"Found {len(breadcrumb_links)} breadcrumb links")
                    
                    # Test clicking on home/first breadcrumb
                    if len(breadcrumb_links) > 0:
                        first_link = breadcrumb_links[0]
                        first_link.click()
                        product_page.wait_for_page_load()
                        logger.info("Successfully clicked on breadcrumb link")
                else:
                    logger.info("No clickable breadcrumb links found")
            else:
                logger.info("Breadcrumbs not found")
        else:
            pytest.skip("Could not navigate to product page")
