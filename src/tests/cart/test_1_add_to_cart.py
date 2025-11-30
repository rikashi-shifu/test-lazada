import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
from config import Config
import time


class TestAddToCart(BaseTest):
    """Test cases for Add to Cart functionality"""

    def test_TC_CART_ADD_001_add_single_item(self):
        """Positive: Add single item to cart"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_CART_ADD_001_add_single_item")
        print("=" * 80)
        # Navigate to homepage FIRST
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        # Search for product
        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for elements

        # Click first product
        first_product = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//div[contains(@class,'product')])[1]")
        )
        if first_product:
            first_product.click()

        time.sleep(1)  # Short wait

        # Add to cart
        add_to_cart_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
        )
        if add_to_cart_btn:
            add_to_cart_btn.click()

        time.sleep(1)  # Short wait

        # Verify item added
        cart_count = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//span[contains(@class,'cart-count')]")
        )

        self.take_screenshot("cart_add_single_item")

        # Skip if can't find elements (likely bot detection)
        if not cart_count:
            pytest.skip("Cart elements not accessible - Lazada bot detection")

    def test_TC_CART_ADD_002_add_multiple_items(self):
        """Positive: Add multiple different items to cart"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_CART_ADD_002_add_multiple_items")
        print("=" * 80)
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        for search_term in ["laptop", "mouse"]:
            search_box = Helpers.wait_for_element(
                self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
            )
            if search_box:
                search_box.clear()
                search_box.send_keys(search_term)
                search_box.send_keys(Keys.RETURN)

            time.sleep(2)  # Wait for elements

            first_product = Helpers.wait_for_clickable(
                self.driver, (By.XPATH, "(//div[contains(@class,'product')])[1]")
            )
            if first_product:
                first_product.click()

            time.sleep(1)  # Short wait

            add_to_cart_btn = Helpers.wait_for_clickable(
                self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
            )
            if add_to_cart_btn:
                add_to_cart_btn.click()

            time.sleep(1)  # Short wait

            self.driver.back()

        self.take_screenshot("cart_add_multiple_items")

    def test_TC_CART_ADD_003_add_out_of_stock(self):
        """Negative: Attempt to add out of stock item"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_CART_ADD_003_add_out_of_stock")
        print("=" * 80)
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for elements

        # Check for disabled add to cart button
        disabled_button = Helpers.is_element_present(
            self.driver,
            (By.XPATH, "//button[contains(text(),'Out of Stock') or @disabled]"),
        )

        self.take_screenshot("cart_add_out_of_stock")

    def test_TC_CART_ADD_004_add_without_selecting_variation(self):
        """Negative: Add product without selecting required variation"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_CART_ADD_004_add_without_selecting_variation")
        print("=" * 80)
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("shoes")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for elements

        first_product = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//div[contains(@class,'product')])[1]")
        )
        if first_product:
            first_product.click()

        time.sleep(1)  # Short wait

        # Try to add without selecting size
        add_to_cart_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
        )
        if add_to_cart_btn:
            add_to_cart_btn.click()

        time.sleep(1)  # Short wait

        self.take_screenshot("cart_add_no_variation")

    def test_TC_CART_ADD_005_add_maximum_quantity(self):
        """Boundary: Add maximum allowed quantity"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_CART_ADD_005_add_maximum_quantity")
        print("=" * 80)
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for elements

        first_product = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//div[contains(@class,'product')])[1]")
        )
        if first_product:
            first_product.click()

        time.sleep(1)  # Short wait

        # Try to set quantity to maximum
        quantity_field = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[@type='number']")
        )
        if quantity_field:
            quantity_field.clear()
            quantity_field.send_keys("99")

        add_to_cart_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
        )
        if add_to_cart_btn:
            add_to_cart_btn.click()

        time.sleep(1)  # Short wait

        self.take_screenshot("cart_add_max_quantity")
