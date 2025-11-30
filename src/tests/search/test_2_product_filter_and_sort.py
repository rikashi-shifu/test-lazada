import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time
from config import Config


class TestProductFilterAndSort(BaseTest):
    """Test cases for Product Filter and Sort functionality"""

    def perform_search_first(self):
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        """Helper to perform initial search"""
        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for elements

    def test_TC_FILTER_001_price_range_filter(self):
        """Positive: Apply price range filter"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_FILTER_001_price_range_filter")
        print("=" * 80)
        # Test Case ID: TC_FILTER_001
        # Objective: Verify price filtering works correctly

        self.perform_search_first()

        # Click price filter
        price_filter = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'Price') or contains(@class,'price-filter')]",
            ),
        )
        if price_filter:
            price_filter.click()

        time.sleep(1)  # Short wait

        # Select price range
        price_option = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//label[contains(text(),'RM 1000 - RM 2000')]")
        )
        if price_option:
            price_option.click()

        time.sleep(2)  # Wait for elements

        self.take_screenshot("filter_price_range")

    def test_TC_FILTER_002_category_filter(self):
        """Positive: Apply category filter"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_FILTER_002_category_filter")
        print("=" * 80)
        # Test Case ID: TC_FILTER_002
        # Objective: Verify category filtering works

        self.perform_search_first()

        category_filter = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//div[contains(text(),'Category')]")
        )
        if category_filter:
            category_filter.click()

        time.sleep(1)  # Short wait

        category_option = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//div[contains(@class,'category-item')])[1]")
        )
        if category_option:
            category_option.click()

        time.sleep(2)  # Wait for elements

        self.take_screenshot("filter_category")

    def test_TC_SORT_001_price_low_to_high(self):
        """Positive: Sort by price ascending"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_SORT_001_price_low_to_high")
        print("=" * 80)
        # Test Case ID: TC_SORT_001
        # Objective: Verify price sorting low to high

        self.perform_search_first()

        sort_dropdown = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//select[contains(@class,'sort')] | //div[contains(text(),'Sort')]",
            ),
        )
        if sort_dropdown:
            sort_dropdown.click()

        time.sleep(1)  # Short wait

        sort_option = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//option[contains(text(),'Price: Low to High')] | //div[contains(text(),'Low to High')]",
            ),
        )
        if sort_option:
            sort_option.click()

        time.sleep(2)  # Wait for elements

        self.take_screenshot("sort_price_asc")

    def test_TC_SORT_002_price_high_to_low(self):
        """Positive: Sort by price descending"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_SORT_002_price_high_to_low")
        print("=" * 80)
        # Test Case ID: TC_SORT_002
        # Objective: Verify price sorting high to low

        self.perform_search_first()

        sort_dropdown = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//select[contains(@class,'sort')] | //div[contains(text(),'Sort')]",
            ),
        )
        if sort_dropdown:
            sort_dropdown.click()

        time.sleep(1)  # Short wait

        sort_option = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//option[contains(text(),'Price: High to Low')] | //div[contains(text(),'High to Low')]",
            ),
        )
        if sort_option:
            sort_option.click()

        time.sleep(2)  # Wait for elements

        self.take_screenshot("sort_price_desc")

    def test_TC_FILTER_003_multiple_filters(self):
        """Positive: Apply multiple filters simultaneously"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_FILTER_003_multiple_filters")
        print("=" * 80)
        # Test Case ID: TC_FILTER_003
        # Objective: Verify multiple filter combination

        self.perform_search_first()

        # Apply price filter
        price_filter = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//div[contains(text(),'Price')]")
        )
        if price_filter:
            price_filter.click()
            time.sleep(1)  # Short wait

            price_option = Helpers.wait_for_clickable(
                self.driver, (By.XPATH, "(//label[contains(@class,'price')])[1]")
            )
            if price_option:
                price_option.click()

        time.sleep(1)  # Short wait

        # Apply brand filter
        brand_filter = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//div[contains(text(),'Brand')]")
        )
        if brand_filter:
            brand_filter.click()
            time.sleep(1)  # Short wait

            brand_option = Helpers.wait_for_clickable(
                self.driver, (By.XPATH, "(//label[contains(@class,'brand')])[1]")
            )
            if brand_option:
                brand_option.click()

        time.sleep(2)  # Wait for elements

        self.take_screenshot("filter_multiple")
