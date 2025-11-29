import pytest
from selenium import webdriver
from config import Config


class BaseTest:
    driver = None

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for each test"""
        self.driver = Config.get_driver()
        self.driver.get(Config.BASE_URL)
        yield
        self.driver.quit()

    def take_screenshot(self, name):
        """Take screenshot for test evidence"""
        import os

        # Create reports directory if it doesn't exist
        os.makedirs("src/reports", exist_ok=True)
        self.driver.save_screenshot(f"src/reports/{name}.png")
