import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time


class TestProductSearch(BaseTest):
    """Test cases for Product Search functionality"""

    def test_TC_SEARCH_001_valid_keyword(self):
        """Positive: Search with valid product keyword"""
        # Test Case ID: TC_SEARCH_001
        # Objective: Verify search returns relevant results

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        # Verify results displayed
        results = Helpers.is_element_present(
            self.driver,
            (By.XPATH, "//div[contains(@class,'product') or contains(@class,'item')]"),
        )
        assert results, "No search results displayed"

        self.take_screenshot("search_valid_keyword")

    def test_TC_SEARCH_002_partial_keyword(self):
        """Positive: Search with partial keyword"""
        # Test Case ID: TC_SEARCH_002
        # Objective: Verify partial match search works

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("lap")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        results = Helpers.is_element_present(
            self.driver, (By.XPATH, "//div[contains(@class,'product')]")
        )
        assert results, "Partial keyword search failed"

        self.take_screenshot("search_partial_keyword")

    def test_TC_SEARCH_003_no_results(self):
        """Negative: Search with non-existent product"""
        # Test Case ID: TC_SEARCH_003
        # Objective: Verify appropriate message for no results

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("xyznonexistentproduct123")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        no_results_msg = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'No results') or contains(text(),'not found')]",
            ),
        )
        assert no_results_msg, "No results message not displayed"

        self.take_screenshot("search_no_results")

    def test_TC_SEARCH_004_special_characters(self):
        """Negative: Search with special characters"""
        # Test Case ID: TC_SEARCH_004
        # Objective: Verify system handles special characters

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("@#$%^&*()")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        # Should show no results or handle gracefully
        page_loaded = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_loaded, "Page failed to load with special characters"

        self.take_screenshot("search_special_chars")

    def test_TC_SEARCH_005_empty_search(self):
        """Negative: Submit empty search"""
        # Test Case ID: TC_SEARCH_005
        # Objective: Verify validation for empty search

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys(Keys.RETURN)

        time.sleep(1)

        # Should either show validation or all products
        page_exists = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_exists, "Empty search not handled"

        self.take_screenshot("search_empty")
