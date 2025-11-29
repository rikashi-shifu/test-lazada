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
        self.driver.save_screenshot(f"src/reports/{name}.png")
