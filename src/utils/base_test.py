import pytest
from selenium import webdriver
from config import Config


class BaseTest:
    driver = None

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for each test"""
        self.driver = Config.get_driver()
        # DON'T navigate to base URL here - let each test navigate where it needs
        # self.driver.get(Config.BASE_URL)
        yield
        try:
            self.driver.quit()
        except Exception:
            pass  # Ignore quit errors

    def take_screenshot(self, name):
        """Take screenshot for test evidence"""
        import os

        os.makedirs("src/reports", exist_ok=True)
        try:
            self.driver.save_screenshot(f"src/reports/{name}.png")
        except Exception:
            pass  # Ignore screenshot errors
