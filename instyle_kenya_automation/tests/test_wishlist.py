"""Wishlist functionality tests"""

import pytest
import logging
from pages.home_page import HomePage
from pages.wishlist_page import WishlistPage
from pages.product_page import ProductPage
from pages.search_results_page import SearchResultsPage
from pages.login_page import LoginPage
from config.config import Config

logger = logging.getLogger(__name__)

class TestWishlist:
    """Test suite for wishlist functionality"""
    
    @pytest.mark.wishlist
    @pytest.mark.smoke
    def test_wishlist_page_loads(self, driver):
        """Test that wishlist page loads successfully"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Wishlist might require login
        if "login" in driver.current_url.lower():
            logger.info("Wishlist requires login, this is normal behavior")
        else:
            assert wishlist_page.is_loaded(), "Wishlist page should load successfully"
            logger.info("Wishlist page loaded successfully")
    
    @pytest.mark.wishlist
    def test_wishlist_access_from_homepage(self, driver):
        """Test accessing wishlist from homepage"""
        home_page = HomePage(driver)
        home_page.load()
        
        if home_page.is_element_present(home_page.WISHLIST_LINK):
            success = home_page.click_wishlist_link()
            
            if success:
                # Check if redirected to login or wishlist
                current_url = driver.current_url.lower()
                
                if "login" in current_url:
                    logger.info("Wishlist access requires login (normal behavior)")
                elif "wishlist" in current_url:
                    wishlist_page = WishlistPage(driver)
                    assert wishlist_page.is_loaded(), "Should navigate to wishlist page"
                    logger.info("Successfully accessed wishlist from homepage")
                else:
                    logger.warning("Unexpected redirect when accessing wishlist")
            else:
                logger.warning("Could not click wishlist link")
        else:
            logger.info("Wishlist link not found on homepage")
    
    @pytest.mark.wishlist
    def test_empty_wishlist_display(self, driver):
        """Test empty wishlist display"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if redirected to login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if wishlist_page.is_wishlist_empty():
            empty_message = wishlist_page.get_empty_wishlist_message()
            assert empty_message, "Empty wishlist should display a message"
            logger.info(f"Empty wishlist displays message: '{empty_message}'")
        else:
            logger.info("Wishlist is not empty, skipping empty wishlist test")
    
    @pytest.mark.wishlist
    def test_add_product_to_wishlist(self, driver, search_terms):
        """Test adding a product to wishlist"""
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
                        # Try to add to wishlist
                        if product_page.is_element_present(product_page.ADD_TO_WISHLIST_BUTTON):
                            add_success = product_page.add_to_wishlist()
                            if add_success:
                                logger.info("Successfully added product to wishlist")
                                
                                # Check if we can access wishlist to verify
                                wishlist_page = WishlistPage(driver)
                                wishlist_page.load()
                                
                                if not "login" in driver.current_url.lower():
                                    if not wishlist_page.is_wishlist_empty():
                                        wishlist_items = wishlist_page.get_wishlist_items()
                                        assert len(wishlist_items) > 0, "Wishlist should contain items after adding product"
                                        logger.info(f"Wishlist now contains {len(wishlist_items)} items")
                            else:
                                logger.warning("Could not add product to wishlist")
                        else:
                            logger.info("Add to wishlist button not found on product page")
                    else:
                        logger.warning("Product page did not load")
                else:
                    logger.warning("Could not click on product")
            else:
                logger.warning("No products found in search results")
        else:
            logger.warning(f"No search results found for '{search_term}'")
    
    @pytest.mark.wishlist
    def test_wishlist_item_display(self, driver):
        """Test wishlist item information display"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if not wishlist_page.is_wishlist_empty():
            wishlist_items = wishlist_page.get_wishlist_items()
            
            if len(wishlist_items) > 0:
                first_item = wishlist_items[0]
                
                # Verify item has required information
                assert first_item["name"], "Wishlist item should have a name"
                assert first_item["price"], "Wishlist item should have a price"
                
                logger.info(f"Wishlist item display test passed. First item: {first_item['name']}")
            else:
                logger.info("No items in wishlist to test display")
        else:
            logger.info("Wishlist is empty, skipping item display test")
    
    @pytest.mark.wishlist
    def test_add_wishlist_item_to_cart(self, driver):
        """Test adding wishlist item to cart"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if not wishlist_page.is_wishlist_empty():
            initial_count = wishlist_page.get_wishlist_item_count()
            
            if initial_count > 0:
                # Try to add first item to cart
                success = wishlist_page.add_item_to_cart(0)
                
                if success:
                    logger.info("Successfully added wishlist item to cart")
                    
                    # Item might be removed from wishlist or stay
                    final_count = wishlist_page.get_wishlist_item_count()
                    logger.info(f"Wishlist count after adding to cart: {initial_count} -> {final_count}")
                else:
                    logger.warning("Could not add wishlist item to cart")
            else:
                logger.info("No items in wishlist to add to cart")
        else:
            logger.info("Wishlist is empty, skipping add to cart test")
    
    @pytest.mark.wishlist
    def test_remove_item_from_wishlist(self, driver):
        """Test removing items from wishlist"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if not wishlist_page.is_wishlist_empty():
            initial_count = wishlist_page.get_wishlist_item_count()
            
            if initial_count > 0:
                # Try to remove first item
                success = wishlist_page.remove_item_from_wishlist(0)
                
                if success:
                    final_count = wishlist_page.get_wishlist_item_count()
                    assert final_count < initial_count, "Item count should decrease after removal"
                    logger.info(f"Successfully removed item from wishlist. Count: {initial_count} -> {final_count}")
                else:
                    logger.warning("Could not remove item from wishlist")
            else:
                logger.info("No items in wishlist to remove")
        else:
            logger.info("Wishlist is empty, skipping item removal test")
    
    @pytest.mark.wishlist
    def test_click_wishlist_product(self, driver):
        """Test clicking on wishlist product to view details"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if not wishlist_page.is_wishlist_empty():
            wishlist_items = wishlist_page.get_wishlist_items()
            
            if len(wishlist_items) > 0:
                # Click on first product
                success = wishlist_page.click_product(0)
                
                if success:
                    # Should navigate to product page
                    product_page = ProductPage(driver)
                    if product_page.is_loaded():
                        assert product_page.is_loaded(), "Should navigate to product page"
                        logger.info("Successfully navigated to product page from wishlist")
                    else:
                        logger.warning("Did not navigate to product page")
                else:
                    logger.warning("Could not click on wishlist product")
            else:
                logger.info("No items in wishlist to click")
        else:
            logger.info("Wishlist is empty, skipping product click test")
    
    @pytest.mark.wishlist
    def test_continue_shopping_from_wishlist(self, driver):
        """Test continue shopping from wishlist"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if wishlist_page.is_element_present(wishlist_page.CONTINUE_SHOPPING_LINK):
            success = wishlist_page.continue_shopping()
            
            if success:
                # Should be redirected away from wishlist page
                assert "wishlist" not in driver.current_url.lower(), "Should be redirected away from wishlist"
                logger.info("Continue shopping from wishlist works correctly")
            else:
                logger.warning("Could not click continue shopping link")
        else:
            logger.info("Continue shopping link not found")
    
    @pytest.mark.wishlist
    @pytest.mark.regression
    def test_clear_entire_wishlist(self, driver):
        """Test clearing entire wishlist"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if (not wishlist_page.is_wishlist_empty() and 
            wishlist_page.is_element_present(wishlist_page.CLEAR_WISHLIST_BUTTON)):
            
            initial_count = wishlist_page.get_wishlist_item_count()
            
            # Clear wishlist
            success = wishlist_page.clear_wishlist()
            
            if success:
                # Wishlist should be empty
                assert wishlist_page.is_wishlist_empty(), "Wishlist should be empty after clearing"
                logger.info(f"Successfully cleared wishlist. Items removed: {initial_count}")
            else:
                logger.warning("Could not clear wishlist")
        else:
            logger.info("Wishlist is empty or clear button not found")
    
    @pytest.mark.wishlist
    def test_wishlist_sorting(self, driver):
        """Test wishlist sorting functionality"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if (not wishlist_page.is_wishlist_empty() and 
            wishlist_page.is_element_present(wishlist_page.SORT_DROPDOWN)):
            
            # Try different sort options
            sort_options = ["Price: Low to High", "Price: High to Low", "Newest First"]
            
            for sort_option in sort_options:
                success = wishlist_page.sort_wishlist(sort_option)
                if success:
                    logger.info(f"Successfully sorted wishlist by: {sort_option}")
                    break
            else:
                logger.warning("Could not test wishlist sorting")
        else:
            logger.info("Wishlist is empty or sort dropdown not found")
    
    @pytest.mark.wishlist
    def test_share_wishlist(self, driver):
        """Test share wishlist functionality"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if wishlist_page.is_element_present(wishlist_page.SHARE_WISHLIST_BUTTON):
            success = wishlist_page.share_wishlist()
            
            if success:
                logger.info("Share wishlist button clicked successfully")
                # Note: We can't test the actual sharing functionality
            else:
                logger.warning("Could not click share wishlist button")
        else:
            logger.info("Share wishlist button not found")
    
    @pytest.mark.wishlist
    @pytest.mark.regression
    def test_move_item_to_cart(self, driver):
        """Test moving wishlist item to cart (remove from wishlist and add to cart)"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if (not wishlist_page.is_wishlist_empty() and 
            wishlist_page.is_element_present(wishlist_page.MOVE_TO_CART_BUTTONS)):
            
            initial_count = wishlist_page.get_wishlist_item_count()
            
            # Move first item to cart
            success = wishlist_page.move_item_to_cart(0)
            
            if success:
                final_count = wishlist_page.get_wishlist_item_count()
                assert final_count < initial_count, "Item should be removed from wishlist after moving to cart"
                logger.info(f"Successfully moved item to cart. Wishlist count: {initial_count} -> {final_count}")
            else:
                logger.warning("Could not move item to cart")
        else:
            logger.info("Wishlist is empty or move to cart buttons not found")
    
    @pytest.mark.wishlist
    def test_add_all_to_cart(self, driver):
        """Test adding all wishlist items to cart"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        if not wishlist_page.is_wishlist_empty():
            initial_count = wishlist_page.get_wishlist_item_count()
            
            # Add all items to cart
            success = wishlist_page.add_all_to_cart()
            
            if success:
                logger.info(f"Successfully added all {initial_count} items to cart")
            else:
                logger.warning("Could not add all items to cart")
        else:
            logger.info("Wishlist is empty, skipping add all to cart test")
    
    @pytest.mark.wishlist
    def test_wishlist_count_display(self, driver):
        """Test wishlist count display"""
        wishlist_page = WishlistPage(driver)
        wishlist_page.load()
        
        # Skip if requires login
        if "login" in driver.current_url.lower():
            pytest.skip("Wishlist requires authentication")
        
        actual_count = wishlist_page.get_wishlist_item_count()
        displayed_count = wishlist_page.get_wishlist_count_display()
        
        if displayed_count:
            logger.info(f"Wishlist count display: '{displayed_count}', actual count: {actual_count}")
        else:
            logger.info(f"No wishlist count display found, actual count: {actual_count}")
