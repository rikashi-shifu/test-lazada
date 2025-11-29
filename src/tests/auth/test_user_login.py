import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time


class TestUserLogin(BaseTest):
    """Test cases for User Login functionality"""

    def test_TC_AUTH_LOGIN_001_valid_credentials(self):
        """Positive: Login with valid email and password"""
        # Test Case ID: TC_AUTH_LOGIN_001
        # Objective: Verify user can login with valid credentials
        # Precondition: User account exists
        # Test Data: Valid email and password

        # Navigate to login page
        login_button = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//a[contains(text(),'Login')]")
        )
        if login_button:
            login_button.click()

        # Enter valid credentials
        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys("testuser@example.com")
        password_field.send_keys("ValidPass123!")
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)

        # Verify login success
        assert Helpers.is_element_present(
            self.driver, (By.XPATH, "//div[contains(@class,'account')]")
        ), "Login failed - user account not displayed"

        self.take_screenshot("login_valid_success")

    def test_TC_AUTH_LOGIN_002_invalid_email(self):
        """Negative: Login with invalid email format"""
        # Test Case ID: TC_AUTH_LOGIN_002
        # Objective: Verify system rejects invalid email format
        # Test Data: Invalid email format (missing @)

        login_button = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//a[contains(text(),'Login')]")
        )
        if login_button:
            login_button.click()

        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys("invalidemail.com")
        password_field.send_keys("ValidPass123!")
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verify error message
        error_present = Helpers.is_element_present(
            self.driver,
            (By.XPATH, "//div[contains(@class,'error') or contains(text(),'invalid')]"),
        )
        assert error_present, "Error message not displayed for invalid email"

        self.take_screenshot("login_invalid_email")

    def test_TC_AUTH_LOGIN_003_wrong_password(self):
        """Negative: Login with incorrect password"""
        # Test Case ID: TC_AUTH_LOGIN_003
        # Objective: Verify system rejects wrong password
        # Test Data: Valid email, incorrect password

        login_button = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//a[contains(text(),'Login')]")
        )
        if login_button:
            login_button.click()

        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys("testuser@example.com")
        password_field.send_keys("WrongPassword123!")
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verify error message
        error_present = Helpers.is_element_present(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'incorrect') or contains(text(),'wrong')]",
            ),
        )
        assert error_present, "Error message not displayed for wrong password"

        self.take_screenshot("login_wrong_password")

    def test_TC_AUTH_LOGIN_004_empty_fields(self):
        """Negative: Login with empty email and password"""
        # Test Case ID: TC_AUTH_LOGIN_004
        # Objective: Verify system validates empty fields
        # Test Data: Empty email and password

        login_button = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//a[contains(text(),'Login')]")
        )
        if login_button:
            login_button.click()

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
                "//div[contains(@class,'validation') or contains(text(),'required')]",
            ),
        )
        assert validation_present, "Validation message not displayed for empty fields"

        self.take_screenshot("login_empty_fields")

    def test_TC_AUTH_LOGIN_005_sql_injection_attempt(self):
        """Negative: Login with SQL injection payload"""
        # Test Case ID: TC_AUTH_LOGIN_005
        # Objective: Verify system prevents SQL injection
        # Test Data: SQL injection string

        login_button = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//a[contains(text(),'Login')]")
        )
        if login_button:
            login_button.click()

        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys("admin'--")
        password_field.send_keys("' OR '1'='1")
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verify login fails
        login_failed = not Helpers.is_element_present(
            self.driver, (By.XPATH, "//div[contains(@class,'account')]")
        )
        assert login_failed, "SQL injection attempt was not prevented"

        self.take_screenshot("login_sql_injection")
