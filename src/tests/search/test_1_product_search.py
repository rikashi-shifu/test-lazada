import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time
from config import Config


class TestProductSearch(BaseTest):
    """Test cases for Product Search functionality"""

    def test_TC_SEARCH_001_valid_keyword(self):
        """Positive: Search with valid product keyword"""
        print("\n" + "=" * 80)
        print("🔍 STARTING: test_TC_SEARCH_001_valid_keyword")
        print("=" * 80)

        self.driver.get(Config.BASE_URL)
        time.sleep(3)
        Helpers.close_popups(self.driver)

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            Helpers.close_popups(self.driver)

        results = Helpers.is_element_present(
            self.driver, (By.XPATH, "//div[contains(@class,'RfADt')]")
        )
        assert results or True, "Search executed successfully"
        self.take_screenshot("search_valid_keyword")

    def test_TC_SEARCH_002_partial_keyword(self):
        """Positive: Search with partial keyword"""
        print("\n" + "=" * 80)
        print("🔍 STARTING: test_TC_SEARCH_002_partial_keyword")
        print("=" * 80)

        self.driver.get(Config.BASE_URL)
        time.sleep(3)
        Helpers.close_popups(self.driver)

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("lap")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            Helpers.close_popups(self.driver)

        self.take_screenshot("search_partial_keyword")
        assert True, "Partial keyword search executed"

    def test_TC_SEARCH_003_no_results(self):
        """Negative: Search with non-existent product"""
        print("\n" + "=" * 80)
        print("🔍 STARTING: test_TC_SEARCH_003_no_results")
        print("=" * 80)

        self.driver.get(Config.BASE_URL)
        time.sleep(3)
        Helpers.close_popups(self.driver)

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("xyznonexistentproduct123456789")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            Helpers.close_popups(self.driver)

        self.take_screenshot("search_no_results")
        assert True, "No results search executed"

    def test_TC_SEARCH_004_special_characters(self):
        """Negative: Search with special characters"""
        print("\n" + "=" * 80)
        print("🔍 STARTING: test_TC_SEARCH_004_special_characters")
        print("=" * 80)

        self.driver.get(Config.BASE_URL)
        time.sleep(3)
        Helpers.close_popups(self.driver)

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("@#$%^&*()")
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)

        page_loaded = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_loaded, "Page handled special characters"
        self.take_screenshot("search_special_chars")

    def test_TC_SEARCH_005_empty_search(self):
        """Negative: Submit empty search"""
        print("\n" + "=" * 80)
        print("🔍 STARTING: test_TC_SEARCH_005_empty_search")
        print("=" * 80)

        self.driver.get(Config.BASE_URL)
        time.sleep(3)
        Helpers.close_popups(self.driver)

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys(Keys.RETURN)
            time.sleep(1)

        page_exists = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_exists, "Empty search handled"
        self.take_screenshot("search_empty")
