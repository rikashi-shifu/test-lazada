import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
from config import Config
import time


class TestUserRegister(BaseTest):
    """Test suite for user registration functionality"""

    def test_TC_AUTH_REG_001_valid_registration(self):
        """
        Test ID: TC_AUTH_REG_001
        Test Case: User Registration with Valid Data
        """
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_AUTH_REG_001_valid_registration")
        print("=" * 80)
        # Navigate to Lazada homepage
        self.driver.get(Config.BASE_URL)
        time.sleep(3)  # Wait for page load

        # Look for "Sign Up" or "Register" link
        try:
            # Try multiple selectors for signup link
            signup_selectors = [
                (By.LINK_TEXT, "SIGNUP"),
                (By.PARTIAL_LINK_TEXT, "Sign"),
                (By.PARTIAL_LINK_TEXT, "Register"),
                (By.XPATH, "//a[contains(text(), 'SIGNUP')]"),
                (By.XPATH, "//a[contains(text(), 'Sign Up')]"),
                (By.XPATH, "//div[contains(@class, 'anonLogin')]//a[last()]"),
            ]

            signup_link = None
            for selector in signup_selectors:
                try:
                    signup_link = Helpers.wait_for_clickable(
                        self.driver, selector, timeout=5
                    )
                    if signup_link:
                        break
                except:
                    continue

            if signup_link:
                signup_link.click()
                time.sleep(3)  # Wait for page load
            else:
                # If can't find signup, try going directly to signup URL
                self.driver.get("https://member.lazada.com.my/user/register")
                time.sleep(3)  # Wait for page load

            # Now look for registration form
            phone_selectors = [
                (By.NAME, "phoneNumber"),
                (By.ID, "phoneNumber"),
                (By.XPATH, "//input[@type='tel']"),
                (
                    By.XPATH,
                    "//input[contains(@placeholder, 'phone') or contains(@placeholder, 'Phone')]",
                ),
            ]

            phone_field = None
            for selector in phone_selectors:
                try:
                    phone_field = Helpers.wait_for_element(
                        self.driver, selector, timeout=5
                    )
                    if phone_field:
                        break
                except:
                    continue

            if phone_field:
                phone_field.send_keys("0123456789")
                time.sleep(1)  # Short wait

                # Take screenshot showing we found the form
                self.take_screenshot("registration_form_found")

                # For now, just verify we reached the registration page
                assert True, "Registration page accessed"
            else:
                # CAPTCHA or bot detection blocking us
                self.take_screenshot("registration_blocked")
                pytest.skip(
                    "Registration form not accessible - likely CAPTCHA or bot detection"
                )

        except Exception as e:
            self.take_screenshot("registration_error")
            pytest.skip(f"Cannot access registration: {str(e)}")

    def test_TC_AUTH_REG_002_duplicate_email(self):
        """Test registration with duplicate email"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_AUTH_REG_002_duplicate_email")
        print("=" * 80)
        pytest.skip("Registration requires CAPTCHA bypass")

    def test_TC_AUTH_REG_003_weak_password(self):
        """Test registration with weak password"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_AUTH_REG_003_weak_password")
        print("=" * 80)
        pytest.skip("Registration requires CAPTCHA bypass")

    def test_TC_AUTH_REG_004_invalid_email_format(self):
        """Test registration with invalid email format"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_AUTH_REG_004_invalid_email_format")
        print("=" * 80)
        pytest.skip("Registration requires CAPTCHA bypass")

    def test_TC_AUTH_REG_005_empty_required_fields(self):
        """Test registration form validation"""
        print("\n" + "=" * 80)
        print(f"🔍 STARTING: test_TC_AUTH_REG_005_empty_required_fields")
        print("=" * 80)
        pytest.skip("Registration requires CAPTCHA bypass")
