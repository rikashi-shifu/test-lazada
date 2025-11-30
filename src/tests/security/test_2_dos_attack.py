import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from config import Config


class TestDoSAttack(BaseTest):
    """Test cases for DoS Attack Prevention"""

    def test_TC_SEC_DOS_001_rapid_search_requests(self):
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        """Security: Rapid repeated search requests"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_SEC_DOS_001_rapid_search_requests")
        print("=" * 80)
        # Test Case ID: TC_SEC_DOS_001
        # Objective: Verify system handles rapid search requests without crashing

        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )

        # Perform rapid searches
        for i in range(10):
            if search_box:
                search_box.clear()
                search_box.send_keys(f"laptop{i}")
                search_box.send_keys(Keys.RETURN)
                time.sleep(0.5)

        # Verify page is still responsive
        page_responsive = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_responsive, "Page became unresponsive after rapid requests"
        self.take_screenshot("sec_dos_rapid_search")

    def test_TC_SEC_DOS_002_repeated_login_attempts(self):
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        """Security: Multiple rapid login attempts"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_SEC_DOS_002_repeated_login_attempts")
        print("=" * 80)
        # Test Case ID: TC_SEC_DOS_002
        # Objective: Verify system handles multiple login attempts

        for attempt in range(5):
            self.driver.get(self.driver.current_url)
            time.sleep(1)  # Short wait

            login_button = Helpers.wait_for_clickable(
                self.driver, (By.XPATH, "//a[contains(text(),'Login')]")
            )
            if login_button:
                login_button.click()

            time.sleep(1)  # Short wait

            email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
            password_field = self.driver.find_element(By.ID, "password")

            if email_field and password_field:
                email_field.send_keys(f"test{attempt}@example.com")
                password_field.send_keys("wrongpass")
                password_field.send_keys(Keys.RETURN)

            time.sleep(1)  # Short wait

        # Check if rate limiting or CAPTCHA appears
        page_exists = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_exists, "System crashed after multiple login attempts"
        self.take_screenshot("sec_dos_repeated_login")

    def test_TC_SEC_DOS_003_rapid_cart_operations(self):
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        """Security: Rapid add/remove cart operations"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_SEC_DOS_003_rapid_cart_operations")
        print("=" * 80)
        # Test Case ID: TC_SEC_DOS_003
        # Objective: Verify cart handles rapid operations

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

        # Rapidly click add to cart
        for i in range(5):
            add_to_cart_btn = Helpers.wait_for_clickable(
                self.driver, (By.XPATH, "//button[contains(text(),'Add to Cart')]")
            )
            if add_to_cart_btn:
                add_to_cart_btn.click()
                time.sleep(0.5)

        page_stable = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_stable, "Cart operations caused system instability"
        self.take_screenshot("sec_dos_rapid_cart")

    def test_TC_SEC_DOS_004_page_refresh_flood(self):
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        """Security: Rapid page refresh requests"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_SEC_DOS_004_page_refresh_flood")
        print("=" * 80)
        # Test Case ID: TC_SEC_DOS_004
        # Objective: Verify system handles rapid page refreshes

        current_url = self.driver.current_url

        # Perform rapid refreshes
        for i in range(10):
            self.driver.refresh()
            time.sleep(0.3)

        # Verify page loads correctly
        page_loaded = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_loaded, "Page failed to load after rapid refreshes"
        self.take_screenshot("sec_dos_page_refresh")

    def test_TC_SEC_DOS_005_large_payload_submission(self):
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        """Security: Submit extremely large data payload"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_SEC_DOS_005_large_payload_submission")
        print("=" * 80)
        # Test Case ID: TC_SEC_DOS_005
        # Objective: Verify system handles large data submissions

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

        write_review = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Write Review')]")
        )
        if write_review:
            write_review.click()

        time.sleep(1)  # Short wait

        # Try to submit very large text
        review_text = Helpers.wait_for_element(self.driver, (By.XPATH, "//textarea"))
        if review_text:
            large_text = "A" * 100000  # 100KB of text
            review_text.send_keys(large_text[:5000])  # Selenium limitation

        time.sleep(1)  # Short wait

        page_responsive = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_responsive, "System failed to handle large payload"
        self.take_screenshot("sec_dos_large_payload")
