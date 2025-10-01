"""Search results page object model"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class SearchResultsPage(BasePage):
    """Search results page object model for instylekenya.co.ke"""
    
    # Search elements
    SEARCH_QUERY_DISPLAY = (By.CSS_SELECTOR, ".search-query, .search-term, .current-search")
    SEARCH_RESULTS_COUNT = (By.CSS_SELECTOR, ".results-count, .search-count, .total-results")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".no-results, .empty-search, .search-empty")
    
    # Product grid
    PRODUCT_GRID = (By.CSS_SELECTOR, ".product-grid, .search-results, .results-grid")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-item, .grid__item, .product-card")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product__title, .product-title, h3")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product__price, .price, .product-price")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".product__image img, .product-image img")
    PRODUCT_LINKS = (By.CSS_SELECTOR, ".product__link, .product-link, a")
    
    # Quick add buttons
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".add-to-cart, .quick-add, button[name*='add']")
    ADD_TO_WISHLIST_BUTTONS = (By.CSS_SELECTOR, ".add-to-wishlist, .wishlist-add")
    
    # Filtering and sorting
    FILTER_SIDEBAR = (By.CSS_SELECTOR, ".filters, .sidebar, .filter-sidebar")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[name*='sort'], .sort-dropdown, .sort-select")
    VIEW_OPTIONS = (By.CSS_SELECTOR, ".view-options, .grid-list-toggle")
    GRID_VIEW_BUTTON = (By.CSS_SELECTOR, ".view-grid, .grid-view")
    LIST_VIEW_BUTTON = (By.CSS_SELECTOR, ".view-list, .list-view")
    
    # Filter categories
    PRICE_FILTERS = (By.CSS_SELECTOR, ".price-filter, .filter-price")
    CATEGORY_FILTERS = (By.CSS_SELECTOR, ".category-filter, .filter-category")
    SIZE_FILTERS = (By.CSS_SELECTOR, ".size-filter, .filter-size")
    COLOR_FILTERS = (By.CSS_SELECTOR, ".color-filter, .filter-color")
    BRAND_FILTERS = (By.CSS_SELECTOR, ".brand-filter, .filter-brand")
    
    # Filter controls
    APPLY_FILTERS_BUTTON = (By.CSS_SELECTOR, ".apply-filters, .filter-apply")
    CLEAR_FILTERS_BUTTON = (By.CSS_SELECTOR, ".clear-filters, .filter-clear")
    FILTER_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")
    
    # Pagination
    PAGINATION = (By.CSS_SELECTOR, ".pagination, .pager")
    PAGINATION_NEXT = (By.CSS_SELECTOR, ".pagination__next, .next, .pager__next")
    PAGINATION_PREV = (By.CSS_SELECTOR, ".pagination__prev, .prev, .pager__prev")
    PAGINATION_NUMBERS = (By.CSS_SELECTOR, ".pagination__number, .page-number")
    
    # Results per page
    RESULTS_PER_PAGE = (By.CSS_SELECTOR, "select[name*='per_page'], .per-page-select")
    
    # Breadcrumbs
    BREADCRUMBS = (By.CSS_SELECTOR, ".breadcrumbs, .breadcrumb")
    
    def __init__(self, driver):
        """Initialize search results page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
    def is_loaded(self) -> bool:
        """Check if search results page is loaded
        
        Returns:
            True if page is loaded, False otherwise
        """
        return ("search" in self.get_current_url().lower() or 
                self.is_element_present(self.PRODUCT_GRID) or 
                self.is_element_present(self.NO_RESULTS_MESSAGE))
    
    def has_results(self) -> bool:
        """Check if search returned results
        
        Returns:
            True if there are search results, False otherwise
        """
        return (len(self.find_elements(self.PRODUCT_ITEMS)) > 0 and 
                not self.is_element_visible(self.NO_RESULTS_MESSAGE))
    
    def get_search_query(self) -> str:
        """Get the search query that was searched for
        
        Returns:
            Search query text
        """
        return self.get_element_text(self.SEARCH_QUERY_DISPLAY)
    
    def get_results_count(self) -> str:
        """Get the number of search results
        
        Returns:
            Results count text
        """
        return self.get_element_text(self.SEARCH_RESULTS_COUNT)
    
    def get_no_results_message(self) -> str:
        """Get no results message
        
        Returns:
            No results message text
        """
        return self.get_element_text(self.NO_RESULTS_MESSAGE)
    
    def get_search_results(self) -> list:
        """Get all search result products
        
        Returns:
            List of product dictionaries
        """
        products = []
        try:
            product_items = self.find_elements(self.PRODUCT_ITEMS)
            
            for item in product_items:
                try:
                    # Get product title
                    title_element = item.find_element(*self.PRODUCT_TITLES)
                    title = title_element.text if title_element else "Unknown Product"
                    
                    # Get product price
                    price_element = item.find_element(*self.PRODUCT_PRICES)
                    price = price_element.text if price_element else "$0.00"
                    
                    # Get product link
                    link_element = item.find_element(*self.PRODUCT_LINKS)
                    link = link_element.get_attribute("href") if link_element else ""
                    
                    # Get image src
                    image_element = item.find_element(*self.PRODUCT_IMAGES)
                    image_src = image_element.get_attribute("src") if image_element else ""
                    
                    products.append({
                        "title": title,
                        "price": price,
                        "link": link,
                        "image_src": image_src
                    })
                    
                except Exception as e:
                    logger.warning(f"Could not extract product info: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to get search results: {str(e)}")
            
        return products
    
    def click_product(self, index: int) -> bool:
        """Click on a product in search results
        
        Args:
            index: Index of the product to click (0-based)
            
        Returns:
            True if product was clicked, False otherwise
        """
        try:
            product_items = self.find_elements(self.PRODUCT_ITEMS)
            
            if index < len(product_items):
                product_items[index].click()
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to click product: {str(e)}")
            return False
    
    def add_product_to_cart(self, index: int) -> bool:
        """Add a product to cart from search results
        
        Args:
            index: Index of the product (0-based)
            
        Returns:
            True if product was added, False otherwise
        """
        try:
            add_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
            
            if index < len(add_buttons):
                add_buttons[index].click()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to add product to cart: {str(e)}")
            return False
    
    def add_product_to_wishlist(self, index: int) -> bool:
        """Add a product to wishlist from search results
        
        Args:
            index: Index of the product (0-based)
            
        Returns:
            True if product was added, False otherwise
        """
        try:
            wishlist_buttons = self.find_elements(self.ADD_TO_WISHLIST_BUTTONS)
            
            if index < len(wishlist_buttons):
                wishlist_buttons[index].click()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to add product to wishlist: {str(e)}")
            return False
    
    def sort_results(self, sort_option: str) -> bool:
        """Sort search results
        
        Args:
            sort_option: Sort option text
            
        Returns:
            True if sorting was applied, False otherwise
        """
        try:
            if self.is_element_present(self.SORT_DROPDOWN):
                from selenium.webdriver.support.ui import Select
                sort_dropdown = Select(self.find_element(self.SORT_DROPDOWN))
                sort_dropdown.select_by_visible_text(sort_option)
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to sort results: {str(e)}")
            return False
    
    def apply_price_filter(self, min_price: str = None, max_price: str = None) -> bool:
        """Apply price filter
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            
        Returns:
            True if filter was applied, False otherwise
        """
        try:
            if self.is_element_present(self.PRICE_FILTERS):
                price_section = self.find_element(self.PRICE_FILTERS)
                
                if min_price:
                    min_input = price_section.find_element(By.CSS_SELECTOR, "input[name*='min'], input[placeholder*='Min']")
                    min_input.clear()
                    min_input.send_keys(min_price)
                
                if max_price:
                    max_input = price_section.find_element(By.CSS_SELECTOR, "input[name*='max'], input[placeholder*='Max']")
                    max_input.clear()
                    max_input.send_keys(max_price)
                
                self.apply_filters()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to apply price filter: {str(e)}")
            return False
    
    def apply_category_filter(self, category: str) -> bool:
        """Apply category filter
        
        Args:
            category: Category name to filter by
            
        Returns:
            True if filter was applied, False otherwise
        """
        try:
            if self.is_element_present(self.CATEGORY_FILTERS):
                category_section = self.find_element(self.CATEGORY_FILTERS)
                
                # Look for checkbox or link with category name
                category_option = category_section.find_element(
                    By.XPATH, f".//input[@value='{category}'] | .//a[contains(text(), '{category}')]"
                )
                category_option.click()
                
                if category_option.tag_name.lower() == 'input':
                    self.apply_filters()
                else:
                    self.wait_for_page_load()
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to apply category filter: {str(e)}")
            return False
    
    def apply_filters(self) -> bool:
        """Apply selected filters
        
        Returns:
            True if filters were applied, False otherwise
        """
        try:
            if self.is_element_present(self.APPLY_FILTERS_BUTTON):
                self.click_element(self.APPLY_FILTERS_BUTTON)
                self.wait_for_page_load()
                return True
            
            # If no apply button, filters might be applied automatically
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply filters: {str(e)}")
            return False
    
    def clear_all_filters(self) -> bool:
        """Clear all applied filters
        
        Returns:
            True if filters were cleared, False otherwise
        """
        try:
            if self.click_element(self.CLEAR_FILTERS_BUTTON):
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to clear filters: {str(e)}")
            return False
    
    def switch_to_grid_view(self) -> bool:
        """Switch to grid view
        
        Returns:
            True if switched to grid view, False otherwise
        """
        return self.click_element(self.GRID_VIEW_BUTTON)
    
    def switch_to_list_view(self) -> bool:
        """Switch to list view
        
        Returns:
            True if switched to list view, False otherwise
        """
        return self.click_element(self.LIST_VIEW_BUTTON)
    
    def go_to_next_page(self) -> bool:
        """Go to next page of results
        
        Returns:
            True if navigated to next page, False otherwise
        """
        if self.click_element(self.PAGINATION_NEXT):
            self.wait_for_page_load()
            return True
        return False
    
    def go_to_previous_page(self) -> bool:
        """Go to previous page of results
        
        Returns:
            True if navigated to previous page, False otherwise
        """
        if self.click_element(self.PAGINATION_PREV):
            self.wait_for_page_load()
            return True
        return False
    
    def go_to_page(self, page_number: int) -> bool:
        """Go to specific page of results
        
        Args:
            page_number: Page number to navigate to
            
        Returns:
            True if navigated to page, False otherwise
        """
        try:
            page_links = self.find_elements(self.PAGINATION_NUMBERS)
            
            for link in page_links:
                if link.text == str(page_number):
                    link.click()
                    self.wait_for_page_load()
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to go to page {page_number}: {str(e)}")
            return False
    
    def set_results_per_page(self, count: int) -> bool:
        """Set number of results per page
        
        Args:
            count: Number of results per page
            
        Returns:
            True if setting was changed, False otherwise
        """
        try:
            if self.is_element_present(self.RESULTS_PER_PAGE):
                from selenium.webdriver.support.ui import Select
                per_page_dropdown = Select(self.find_element(self.RESULTS_PER_PAGE))
                per_page_dropdown.select_by_visible_text(str(count))
                self.wait_for_page_load()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to set results per page: {str(e)}")
            return False
