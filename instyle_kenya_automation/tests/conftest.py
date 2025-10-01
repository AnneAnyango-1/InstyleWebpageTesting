import pytest
from utils.driver_factory import DriverFactory

@pytest.fixture
def driver():
    """Create and return WebDriver instance."""
    driver_instance = DriverFactory.create_driver()
    yield driver_instance
    driver_instance.quit()
