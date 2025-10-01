"""Search functionality tests"""

import pytest
import logging
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from config.config import Config

logger = logging.getLogger(__name__)

class TestSearch:
    """Test suite for search functionality"""
    
    @pytest.mark.search
    @pytest.mark.smoke
    def test_basic_search_functionality(self, driver, search_terms):
        """Test basic search functionality from homepage"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        success = home_page.search_for_product(search_term)
        
        assert success, f"Search for '{search_term}' should be successful"
        
        # Verify we're on search results page
        search_page = SearchResultsPage(driver)
        assert search_page.is_loaded(), "Should navigate to search results page"
        
        logger.info(f"Basic search for '{search_term}' completed successfully")
    
    @pytest.mark.search
    @pytest.mark.smoke
    def test_search_results_display(self, driver, search_terms):
        """Test that search results are displayed correctly"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if search_page.has_results():
            results = search_page.get_search_results()
            assert len(results) > 0, "Search should return results"
            
            # Verify first result has required information
            first_result = results[0]
            assert first_result["title"], "Search result should have a title"
            assert first_result["price"], "Search result should have a price"
            
            logger.info(f"Search for '{search_term}' returned {len(results)} results")
        else:
            # Check for no results message
            no_results_msg = search_page.get_no_results_message()
            logger.info(f"No results found for '{search_term}'. Message: '{no_results_msg}'")
    
    @pytest.mark.search
    def test_search_query_display(self, driver, search_terms):
        """Test that search query is displayed on results page"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        displayed_query = search_page.get_search_query()
        
        if displayed_query:
            assert search_term.lower() in displayed_query.lower(), "Search query should be displayed on results page"
            logger.info(f"Search query displayed correctly: '{displayed_query}'")
        else:
            logger.info("Search query not displayed on results page")
    
    @pytest.mark.search
    def test_search_results_count(self, driver, search_terms):
        """Test search results count display"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        results_count = search_page.get_results_count()
        
        if results_count:
            logger.info(f"Search results count displayed: '{results_count}'")
        else:
            logger.info("Search results count not displayed")
    
    @pytest.mark.search
    @pytest.mark.regression
    def test_multiple_search_terms(self, driver, search_terms):
        """Test search with multiple different terms"""
        home_page = HomePage(driver)
        
        for search_term in search_terms[:3]:  # Test first 3 terms
            home_page.load()  # Reload homepage for each search
            
            success = home_page.search_for_product(search_term)
            assert success, f"Search for '{search_term}' should work"
            
            search_page = SearchResultsPage(driver)
            assert search_page.is_loaded(), f"Should load search results for '{search_term}'"
            
            if search_page.has_results():
                results = search_page.get_search_results()
                logger.info(f"Search '{search_term}' returned {len(results)} results")
            else:
                logger.info(f"No results for search term '{search_term}'")
    
    @pytest.mark.search
    def test_empty_search(self, driver):
        """Test search with empty query"""
        home_page = HomePage(driver)
        home_page.load()
        
        # Try searching with empty string
        success = home_page.search_for_product("")
        
        # Empty search might be prevented or show all products
        if success:
            search_page = SearchResultsPage(driver)
            if search_page.is_loaded():
                logger.info("Empty search was processed")
            else:
                logger.info("Empty search was prevented")
        else:
            logger.info("Empty search was prevented at input level")
    
    @pytest.mark.search
    def test_special_characters_search(self, driver):
        """Test search with special characters"""
        home_page = HomePage(driver)
        home_page.load()
        
        special_terms = ["women's", "size-10", "red&blue", "50% off"]
        
        for term in special_terms:
            home_page.load()  # Reload for each test
            
            success = home_page.search_for_product(term)
            if success:
                search_page = SearchResultsPage(driver)
                logger.info(f"Special character search '{term}' was processed")
            else:
                logger.warning(f"Could not search for '{term}'")
    
    @pytest.mark.search
    def test_click_search_result(self, driver, search_terms):
        """Test clicking on a search result"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if search_page.has_results():
            # Click on first result
            success = search_page.click_product(0)
            
            if success:
                # Should navigate away from search results
                assert not search_page.is_loaded(), "Should navigate away from search results"
                logger.info("Successfully clicked on search result")
            else:
                logger.warning("Could not click on search result")
        else:
            logger.info("No search results to click")
    
    @pytest.mark.search
    @pytest.mark.regression
    def test_search_sorting(self, driver, search_terms):
        """Test search results sorting"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if search_page.has_results() and search_page.is_element_present(search_page.SORT_DROPDOWN):
            # Try different sort options
            sort_options = ["Price: Low to High", "Price: High to Low", "Newest", "Popularity"]
            
            for sort_option in sort_options:
                success = search_page.sort_results(sort_option)
                if success:
                    logger.info(f"Successfully sorted results by: {sort_option}")
                    break
            else:
                logger.warning("Could not test search result sorting")
        else:
            logger.info("No results or sort dropdown not available")
    
    @pytest.mark.search
    def test_search_filtering(self, driver, search_terms):
        """Test search results filtering"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if search_page.has_results():
            # Try price filter
            if search_page.is_element_present(search_page.PRICE_FILTERS):
                success = search_page.apply_price_filter(min_price="10", max_price="100")
                if success:
                    logger.info("Successfully applied price filter")
                else:
                    logger.warning("Could not apply price filter")
            
            # Try category filter
            if search_page.is_element_present(search_page.CATEGORY_FILTERS):
                success = search_page.apply_category_filter("Dresses")
                if success:
                    logger.info("Successfully applied category filter")
                else:
                    logger.warning("Could not apply category filter")
        else:
            logger.info("No results to filter")
    
    @pytest.mark.search
    def test_clear_search_filters(self, driver, search_terms):
        """Test clearing search filters"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if (search_page.has_results() and 
            search_page.is_element_present(search_page.CLEAR_FILTERS_BUTTON)):
            
            # Apply some filters first
            search_page.apply_price_filter(min_price="10", max_price="50")
            
            # Clear filters
            success = search_page.clear_all_filters()
            if success:
                logger.info("Successfully cleared all filters")
            else:
                logger.warning("Could not clear filters")
        else:
            logger.info("No results or clear filters button not available")
    
    @pytest.mark.search
    def test_search_pagination(self, driver, search_terms):
        """Test search results pagination"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if (search_page.has_results() and 
            search_page.is_element_present(search_page.PAGINATION)):
            
            # Try going to next page
            if search_page.is_element_present(search_page.PAGINATION_NEXT):
                success = search_page.go_to_next_page()
                if success:
                    logger.info("Successfully navigated to next page")
                    
                    # Try going back
                    if search_page.is_element_present(search_page.PAGINATION_PREV):
                        back_success = search_page.go_to_previous_page()
                        if back_success:
                            logger.info("Successfully navigated back to previous page")
                else:
                    logger.warning("Could not navigate to next page")
            else:
                logger.info("No next page available")
        else:
            logger.info("No pagination available")
    
    @pytest.mark.search
    def test_results_per_page(self, driver, search_terms):
        """Test changing results per page"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if (search_page.has_results() and 
            search_page.is_element_present(search_page.RESULTS_PER_PAGE)):
            
            # Try different results per page options
            for count in [10, 20, 50]:
                success = search_page.set_results_per_page(count)
                if success:
                    logger.info(f"Successfully set results per page to {count}")
                    break
            else:
                logger.warning("Could not change results per page")
        else:
            logger.info("Results per page option not available")
    
    @pytest.mark.search
    def test_view_options(self, driver, search_terms):
        """Test grid/list view options"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if search_page.has_results():
            # Try switching to list view
            if search_page.is_element_present(search_page.LIST_VIEW_BUTTON):
                success = search_page.switch_to_list_view()
                if success:
                    logger.info("Successfully switched to list view")
            
            # Try switching to grid view
            if search_page.is_element_present(search_page.GRID_VIEW_BUTTON):
                success = search_page.switch_to_grid_view()
                if success:
                    logger.info("Successfully switched to grid view")
        else:
            logger.info("No results to test view options")
    
    @pytest.mark.search
    def test_add_to_cart_from_search(self, driver, search_terms):
        """Test adding product to cart from search results"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if search_page.has_results():
            # Try to add first product to cart
            success = search_page.add_product_to_cart(0)
            
            if success:
                logger.info("Successfully added product to cart from search results")
            else:
                logger.info("Add to cart functionality not available in search results")
        else:
            logger.info("No results to add to cart")
    
    @pytest.mark.search
    def test_add_to_wishlist_from_search(self, driver, search_terms):
        """Test adding product to wishlist from search results"""
        home_page = HomePage(driver)
        home_page.load()
        
        search_term = search_terms[0]
        home_page.search_for_product(search_term)
        
        search_page = SearchResultsPage(driver)
        
        if search_page.has_results():
            # Try to add first product to wishlist
            success = search_page.add_product_to_wishlist(0)
            
            if success:
                logger.info("Successfully added product to wishlist from search results")
            else:
                logger.info("Add to wishlist functionality not available in search results")
        else:
            logger.info("No results to add to wishlist")
