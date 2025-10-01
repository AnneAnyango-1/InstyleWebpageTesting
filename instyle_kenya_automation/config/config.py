"""Configuration settings for the test automation framework"""

import os
from typing import Dict, Any

class Config:
    """Main configuration class containing all test settings"""
    
    # Base URL
    BASE_URL = "https://instylekenya.co.ke/"
    
    # Browser settings
    DEFAULT_BROWSER = "chrome"
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    
    # Screen resolution
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    
    # Test data
    TEST_USER = {
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+254700000000"
    }
    
    # URLs for different pages
    URLS = {
        "home": BASE_URL,
        "login": f"{BASE_URL}account/login",
        "register": f"{BASE_URL}account/register",
        "cart": f"{BASE_URL}cart",
        "wishlist": f"{BASE_URL}account/wishlist",
        "contact": f"{BASE_URL}pages/contact-us",
        "about": f"{BASE_URL}pages/about-us"
    }
    
    # Search terms for testing
    SEARCH_TERMS = [
        "dress",
        "shoes",
        "handbag",
        "jewelry",
        "accessories"
    ]
    
    # Product categories
    CATEGORIES = [
        "Dresses",
        "Shoes",
        "Bags",
        "Jewelry",
        "Accessories"
    ]
    
    @staticmethod
    def get_browser_options(browser_name: str) -> Dict[str, Any]:
        """Get browser-specific options"""
        options = {
            "chrome": {
                "arguments": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--window-size=1920,1080"
                ]
            },
            "firefox": {
                "arguments": [
                    "--width=1920",
                    "--height=1080"
                ]
            }
        }
        
        if Config.HEADLESS:
            if browser_name == "chrome":
                options["chrome"]["arguments"].append("--headless")
            elif browser_name == "firefox":
                options["firefox"]["arguments"].append("--headless")
        
        return options.get(browser_name, {"arguments": []})
