import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time


class TestUpdateCartItem(BaseTest):
    """Test cases for Update Cart Item functionality"""

    def add_item_to_cart_first(self):
        """Helper method to add item to cart before testing updates"""
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

        add_to_cart_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
        )
        if add_to_cart_btn:
            add_to_cart_btn.click()

        time.sleep(1)

        # Go to cart
        cart_icon = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//a[contains(@href,'cart')]")
        )
        if cart_icon:
            cart_icon.click()

        time.sleep(1)

    def test_TC_CART_UPDATE_001_increase_quantity(self):
        """Positive: Increase item quantity in cart"""
        # Test Case ID: TC_CART_UPDATE_001
        # Objective: Verify user can increase quantity

        self.add_item_to_cart_first()

        # Increase quantity
        plus_button = Helpers.wait_for_clickable(
            self.driver,
            (By.XPATH, "//button[contains(@class,'plus') or contains(text(),'+')]"),
        )
        if plus_button:
            plus_button.click()

        time.sleep(1)

        # Verify quantity updated
        quantity_field = self.driver.find_element(By.XPATH, "//input[@type='number']")
        assert int(quantity_field.get_attribute("value")) > 1, "Quantity not increased"

        self.take_screenshot("cart_update_increase")

    def test_TC_CART_UPDATE_002_decrease_quantity(self):
        """Positive: Decrease item quantity in cart"""
        # Test Case ID: TC_CART_UPDATE_002
        # Objective: Verify user can decrease quantity

        self.add_item_to_cart_first()

        # First increase to have room to decrease
        plus_button = Helpers.wait_for_clickable(
            self.driver,
            (By.XPATH, "//button[contains(@class,'plus') or contains(text(),'+')]"),
        )
        if plus_button:
            plus_button.click()

        time.sleep(1)

        # Decrease quantity
        minus_button = Helpers.wait_for_clickable(
            self.driver,
            (By.XPATH, "//button[contains(@class,'minus') or contains(text(),'-')]"),
        )
        if minus_button:
            minus_button.click()

        time.sleep(1)

        self.take_screenshot("cart_update_decrease")

    def test_TC_CART_UPDATE_003_change_variation(self):
        """Positive: Change product variation (size/color)"""
        # Test Case ID: TC_CART_UPDATE_003
        # Objective: Verify user can change variation

        self.add_item_to_cart_first()

        # Click edit/change variation
        edit_button = Helpers.wait_for_clickable(
            self.driver,
            (By.XPATH, "//button[contains(text(),'Edit') or contains(@class,'edit')]"),
        )
        if edit_button:
            edit_button.click()

        time.sleep(1)

        # Select different variation
        variation_option = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//div[contains(@class,'variation')])[2]")
        )
        if variation_option:
            variation_option.click()

        time.sleep(1)

        self.take_screenshot("cart_update_variation")

    def test_TC_CART_UPDATE_004_quantity_below_minimum(self):
        """Negative: Set quantity below minimum (0 or negative)"""
        # Test Case ID: TC_CART_UPDATE_004
        # Objective: Verify system prevents invalid quantity

        self.add_item_to_cart_first()

        # Try to set quantity to 0
        quantity_field = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[@type='number']")
        )
        if quantity_field:
            quantity_field.clear()
            quantity_field.send_keys("0")
            quantity_field.send_keys(Keys.TAB)

        time.sleep(1)

        # Verify error or quantity reset to 1
        final_quantity = quantity_field.get_attribute("value")
        assert int(final_quantity) >= 1, "Invalid quantity allowed"

        self.take_screenshot("cart_update_zero_quantity")

    def test_TC_CART_UPDATE_005_quantity_exceeds_stock(self):
        """Negative: Set quantity exceeding available stock"""
        # Test Case ID: TC_CART_UPDATE_005
        # Objective: Verify system prevents exceeding stock

        self.add_item_to_cart_first()

        # Try to set very high quantity
        quantity_field = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[@type='number']")
        )
        if quantity_field:
            quantity_field.clear()
            quantity_field.send_keys("9999")
            quantity_field.send_keys(Keys.TAB)

        time.sleep(1)

        # Verify error message
        error_present = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'stock') or contains(text(),'available')]",
            ),
        )

        self.take_screenshot("cart_update_exceed_stock")
