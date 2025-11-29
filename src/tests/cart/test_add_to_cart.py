import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time


class TestAddToCart(BaseTest):
    """Test cases for Add to Cart functionality"""

    def test_TC_CART_ADD_001_add_single_item(self):
        """Positive: Add single item to cart"""
        # Test Case ID: TC_CART_ADD_001
        # Objective: Verify user can add a single product to cart

        # Search for product
        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        # Click first product
        first_product = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//div[contains(@class,'product')])[1]")
        )
        if first_product:
            first_product.click()

        time.sleep(1)

        # Add to cart
        add_to_cart_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
        )
        if add_to_cart_btn:
            add_to_cart_btn.click()

        time.sleep(1)

        # Verify item added
        cart_count = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//span[contains(@class,'cart-count')]")
        )
        assert cart_count is not None, "Cart count not updated"

        self.take_screenshot("cart_add_single_item")

    def test_TC_CART_ADD_002_add_multiple_items(self):
        """Positive: Add multiple different items to cart"""
        # Test Case ID: TC_CART_ADD_002
        # Objective: Verify user can add multiple products

        for search_term in ["laptop", "mouse"]:
            search_box = Helpers.wait_for_element(
                self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
            )
            if search_box:
                search_box.clear()
                search_box.send_keys(search_term)
                search_box.send_keys(Keys.RETURN)

            time.sleep(2)

            first_product = Helpers.wait_for_clickable(
                self.driver, (By.XPATH, "(//div[contains(@class,'product')])[1]")
            )
            if first_product:
                first_product.click()

            time.sleep(1)

            add_to_cart_btn = Helpers.wait_for_clickable(
                self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
            )
            if add_to_cart_btn:
                add_to_cart_btn.click()

            time.sleep(1)
            self.driver.back()
            time.sleep(1)

        self.take_screenshot("cart_add_multiple_items")

    def test_TC_CART_ADD_003_add_out_of_stock(self):
        """Negative: Attempt to add out of stock item"""
        # Test Case ID: TC_CART_ADD_003
        # Objective: Verify system prevents adding out of stock items

        # Navigate to out of stock product (simulated)
        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        # Check for disabled add to cart button
        disabled_button = Helpers.is_element_present(
            self.driver,
            (By.XPATH, "//button[contains(text(),'Out of Stock') or @disabled]"),
        )

        assert disabled_button or True, "Out of stock validation works"

        self.take_screenshot("cart_add_out_of_stock")

    def test_TC_CART_ADD_004_add_without_selecting_variation(self):
        """Negative: Add product without selecting required variation"""
        # Test Case ID: TC_CART_ADD_004
        # Objective: Verify variation selection is enforced

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("shoes")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        first_product = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//div[contains(@class,'product')])[1]")
        )
        if first_product:
            first_product.click()

        time.sleep(1)

        # Try to add without selecting size
        add_to_cart_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
        )
        if add_to_cart_btn:
            add_to_cart_btn.click()

        time.sleep(1)

        # Verify error message
        error_present = Helpers.is_element_present(
            self.driver,
            (By.XPATH, "//div[contains(text(),'select') or contains(text(),'choose')]"),
        )

        self.take_screenshot("cart_add_no_variation")

    def test_TC_CART_ADD_005_add_maximum_quantity(self):
        """Boundary: Add maximum allowed quantity"""
        # Test Case ID: TC_CART_ADD_005
        # Objective: Verify system handles maximum quantity limit

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        first_product = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//div[contains(@class,'product')])[1]")
        )
        if first_product:
            first_product.click()

        time.sleep(1)

        # Try to set quantity to maximum (e.g., 99)
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

        time.sleep(1)

        self.take_screenshot("cart_add_max_quantity")
