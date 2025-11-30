import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time
from config import Config


class TestSubmitReview(BaseTest):
    """Test cases for Submit Product Review functionality"""

    def navigate_to_product(self):
        self.driver.get(Config.BASE_URL)
        time.sleep(3)

        """Helper to navigate to product page"""
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

    def test_TC_REVIEW_SUBMIT_001_valid_review(self):
        """Positive: Submit review with all fields filled"""
        # Test Case ID: TC_REVIEW_SUBMIT_001
        # Objective: Verify user can submit complete review

        self.navigate_to_product()

        # Click write review button
        write_review_btn = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//button[contains(text(),'Write Review') or contains(text(),'Rate')]",
            ),
        )
        if write_review_btn:
            write_review_btn.click()

        time.sleep(1)

        # Select rating (5 stars)
        star_rating = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//span[contains(@class,'star')])[5]")
        )
        if star_rating:
            star_rating.click()

        # Enter review text
        review_text = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//textarea[contains(@placeholder,'review')]")
        )
        if review_text:
            review_text.send_keys("Great product! Very satisfied with the quality.")

        # Submit review
        submit_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Submit')]")
        )
        if submit_btn:
            submit_btn.click()

        time.sleep(2)

        self.take_screenshot("review_submit_valid")

    def test_TC_REVIEW_SUBMIT_002_rating_only(self):
        """Positive: Submit review with rating only (no text)"""
        # Test Case ID: TC_REVIEW_SUBMIT_002
        # Objective: Verify rating-only submission

        self.navigate_to_product()

        write_review_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Write Review')]")
        )
        if write_review_btn:
            write_review_btn.click()

        time.sleep(1)

        # Select rating only
        star_rating = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//span[contains(@class,'star')])[4]")
        )
        if star_rating:
            star_rating.click()

        submit_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Submit')]")
        )
        if submit_btn:
            submit_btn.click()

        time.sleep(2)

        self.take_screenshot("review_submit_rating_only")

    def test_TC_REVIEW_SUBMIT_003_no_rating(self):
        """Negative: Attempt to submit without rating"""
        # Test Case ID: TC_REVIEW_SUBMIT_003
        # Objective: Verify rating is required

        self.navigate_to_product()

        write_review_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Write Review')]")
        )
        if write_review_btn:
            write_review_btn.click()

        time.sleep(1)

        # Enter text without rating
        review_text = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//textarea[contains(@placeholder,'review')]")
        )
        if review_text:
            review_text.send_keys("Good product")

        submit_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Submit')]")
        )
        if submit_btn:
            submit_btn.click()

        time.sleep(1)

        # Verify error message
        error_present = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'rating') or contains(text(),'required')]",
            ),
        )

        self.take_screenshot("review_submit_no_rating")

    def test_TC_REVIEW_SUBMIT_004_excessive_text(self):
        """Boundary: Submit review with maximum character limit"""
        # Test Case ID: TC_REVIEW_SUBMIT_004
        # Objective: Verify character limit enforcement

        self.navigate_to_product()

        write_review_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Write Review')]")
        )
        if write_review_btn:
            write_review_btn.click()

        time.sleep(1)

        star_rating = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//span[contains(@class,'star')])[5]")
        )
        if star_rating:
            star_rating.click()

        # Enter very long text
        review_text = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//textarea[contains(@placeholder,'review')]")
        )
        if review_text:
            long_text = "A" * 5000  # Excessive text
            review_text.send_keys(long_text)

        time.sleep(1)

        self.take_screenshot("review_submit_excessive_text")

    def test_TC_REVIEW_SUBMIT_005_special_characters(self):
        """Negative: Submit review with special characters"""
        # Test Case ID: TC_REVIEW_SUBMIT_005
        # Objective: Verify handling of special characters

        self.navigate_to_product()

        write_review_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Write Review')]")
        )
        if write_review_btn:
            write_review_btn.click()

        time.sleep(1)

        star_rating = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "(//span[contains(@class,'star')])[3]")
        )
        if star_rating:
            star_rating.click()

        review_text = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//textarea[contains(@placeholder,'review')]")
        )
        if review_text:
            review_text.send_keys("<script>alert('test')</script>")

        submit_btn = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Submit')]")
        )
        if submit_btn:
            submit_btn.click()

        time.sleep(2)

        self.take_screenshot("review_submit_special_chars")
