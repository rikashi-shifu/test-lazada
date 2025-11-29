import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time
import random
import string


class TestUserRegister(BaseTest):
    """Test cases for User Registration functionality"""

    def generate_random_email(self):
        """Generate random email for testing"""
        random_str = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )
        return f"testuser_{random_str}@example.com"

    def test_TC_AUTH_REG_001_valid_registration(self):
        """Positive: Register with valid data"""
        # Test Case ID: TC_AUTH_REG_001
        # Objective: Verify user can register with valid information

        register_button = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//a[contains(text(),'Sign Up') or contains(text(),'Register')]",
            ),
        )
        if register_button:
            register_button.click()

        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys(self.generate_random_email())
        password_field.send_keys("ValidPass123!")
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)

        # Verify registration success
        success = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'success') or contains(@class,'success')]",
            ),
        )
        assert success, "Registration failed"

        self.take_screenshot("register_valid")

    def test_TC_AUTH_REG_002_duplicate_email(self):
        """Negative: Register with existing email"""
        # Test Case ID: TC_AUTH_REG_002
        # Objective: Verify system prevents duplicate email registration

        register_button = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//a[contains(text(),'Sign Up') or contains(text(),'Register')]",
            ),
        )
        if register_button:
            register_button.click()

        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys("testuser@example.com")
        password_field.send_keys("ValidPass123!")
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verify error message
        error_present = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'already exists') or contains(text(),'taken')]",
            ),
        )
        assert error_present, "Duplicate email error not shown"

        self.take_screenshot("register_duplicate_email")

    def test_TC_AUTH_REG_003_weak_password(self):
        """Negative: Register with weak password"""
        # Test Case ID: TC_AUTH_REG_003
        # Objective: Verify system enforces password strength

        register_button = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//a[contains(text(),'Sign Up') or contains(text(),'Register')]",
            ),
        )
        if register_button:
            register_button.click()

        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys(self.generate_random_email())
        password_field.send_keys("123")
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verify password strength error
        error_present = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'password') and (contains(text(),'weak') or contains(text(),'strong'))]",
            ),
        )
        assert error_present, "Weak password error not shown"

        self.take_screenshot("register_weak_password")

    def test_TC_AUTH_REG_004_invalid_email_format(self):
        """Negative: Register with invalid email format"""
        # Test Case ID: TC_AUTH_REG_004
        # Objective: Verify email format validation

        register_button = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//a[contains(text(),'Sign Up') or contains(text(),'Register')]",
            ),
        )
        if register_button:
            register_button.click()

        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys("invalid-email")
        password_field.send_keys("ValidPass123!")
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verify validation error
        error_present = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'valid email') or contains(text(),'email format')]",
            ),
        )
        assert error_present, "Email format error not shown"

        self.take_screenshot("register_invalid_email")

    def test_TC_AUTH_REG_005_empty_required_fields(self):
        """Negative: Register with empty required fields"""
        # Test Case ID: TC_AUTH_REG_005
        # Objective: Verify required field validation

        register_button = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//a[contains(text(),'Sign Up') or contains(text(),'Register')]",
            ),
        )
        if register_button:
            register_button.click()

        submit_button = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[@type='submit']")
        )
        if submit_button:
            submit_button.click()

        time.sleep(1)

        # Verify validation messages
        validation_present = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'required') or contains(@class,'validation')]",
            ),
        )
        assert validation_present, "Required field validation not shown"

        self.take_screenshot("register_empty_fields")
