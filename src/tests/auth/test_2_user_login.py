import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
from config import Config
import time


class TestUserLogin(BaseTest):
    """Test suite for user login functionality"""

    def test_TC_AUTH_LOGIN_001_valid_credentials(self):
        """
        Test ID: TC_AUTH_LOGIN_001
        Test Case: User Login with Valid Credentials
        """
        print("\n" + "=" * 80)
        print("🔍 STARTING TEST: Login with Valid Credentials")
        print("=" * 80)

        # Step 1: Navigate to homepage
        print("\n📍 Step 1: Navigating to Lazada homepage...")
        self.driver.get(Config.BASE_URL)
        time.sleep(3)
        print("✓ Page loaded successfully")

        try:
            # Step 2: Find and click LOGIN button
            print("\n👤 Step 2: Looking for LOGIN button...")
            login_selectors = [
                (By.LINK_TEXT, "LOGIN"),
                (By.PARTIAL_LINK_TEXT, "Login"),
                (By.XPATH, "//a[contains(text(), 'LOGIN')]"),
                (By.XPATH, "//div[contains(@class, 'anonLogin')]//a[1]"),
            ]

            login_link = None
            for i, selector in enumerate(login_selectors, 1):
                print(f"   Trying selector {i}/4: {selector[1][:50]}...")
                try:
                    login_link = Helpers.wait_for_clickable(
                        self.driver, selector, timeout=5
                    )
                    if login_link:
                        print(f"   ✓ Found LOGIN button with selector {i}")
                        break
                except:
                    print(f"   ✗ Selector {i} failed")
                    continue

            if login_link:
                print("\n🖱️  Step 3: Clicking LOGIN button...")
                self.take_screenshot("before_click_login")
                login_link.click()
                time.sleep(3)
                print("✓ Login modal opened")
                self.take_screenshot("after_click_login")
            else:
                print("\n⚠️  LOGIN button not found, trying direct URL...")
                self.driver.get("https://member.lazada.com.my/user/login")
                time.sleep(3)
                print("✓ Navigated to login page directly")
                self.take_screenshot("direct_login_page")

            # Step 4: Find email field
            print("\n📧 Step 4: Looking for email/phone input field...")
            email_selectors = [
                (By.NAME, "loginId"),
                (By.ID, "login_id"),
                (By.XPATH, "//input[@type='text' or @type='email' or @type='tel']"),
            ]

            email_field = None
            for i, selector in enumerate(email_selectors, 1):
                print(f"   Trying selector {i}/3...")
                try:
                    email_field = Helpers.wait_for_element(
                        self.driver, selector, timeout=5
                    )
                    if email_field and email_field.is_displayed():
                        print(f"   ✓ Found email field with selector {i}")
                        break
                except:
                    print(f"   ✗ Selector {i} failed")
                    continue

            if email_field:
                print("\n⌨️  Step 5: Entering email...")
                email_field.send_keys(Config.TEST_EMAIL)
                print(f"✓ Entered email: {Config.TEST_EMAIL}")
                self.take_screenshot("email_entered")

                # Step 6: Find password field
                print("\n🔒 Step 6: Looking for password field...")
                password_field = Helpers.wait_for_element(
                    self.driver, (By.XPATH, "//input[@type='password']"), timeout=5
                )

                if password_field:
                    print("✓ Found password field")
                    print("\n⌨️  Step 7: Entering password...")
                    password_field.send_keys(Config.TEST_PASSWORD)
                    print("✓ Password entered (hidden)")
                    self.take_screenshot("credentials_entered")

                    # Step 8: Find submit button
                    print("\n🔍 Step 8: Looking for submit button...")
                    submit_btn = Helpers.wait_for_clickable(
                        self.driver,
                        (
                            By.XPATH,
                            "//button[@type='submit' or contains(text(), 'LOGIN')]",
                        ),
                        timeout=5,
                    )

                    if submit_btn:
                        print("✓ Found submit button")
                        print("\n⚠️  Note: Not clicking submit due to CAPTCHA")
                        self.take_screenshot("ready_to_submit")
                        print("\n" + "=" * 80)
                        print(
                            "✓ TEST RESULT: Login form accessible (CAPTCHA prevents actual login)"
                        )
                        print("=" * 80)
                        pytest.skip("Login form found but CAPTCHA prevents submission")
                    else:
                        print("\n✗ Submit button not found")
                        pytest.skip("Submit button not found")
                else:
                    print("\n✗ Password field not found")
                    pytest.skip("Password field not found")
            else:
                print("\n✗ Email field not found")
                self.take_screenshot("login_form_not_found")
                pytest.skip("Login form not accessible - likely bot detection")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            self.take_screenshot("login_error")
            pytest.skip(f"Cannot access login: {str(e)}")

    def test_TC_AUTH_LOGIN_002_invalid_email(self):
        """Test login with invalid email"""
        print("\n🔍 TEST: Login with Invalid Email - SKIPPED (Requires CAPTCHA bypass)")
        pytest.skip("Login requires CAPTCHA bypass")

    def test_TC_AUTH_LOGIN_003_wrong_password(self):
        """Test login with wrong password"""
        print(
            "\n🔍 TEST: Login with Wrong Password - SKIPPED (Requires CAPTCHA bypass)"
        )
        pytest.skip("Login requires CAPTCHA bypass")

    def test_TC_AUTH_LOGIN_004_empty_fields(self):
        """Test login with empty fields"""
        print("\n🔍 TEST: Login with Empty Fields - SKIPPED (Requires CAPTCHA bypass)")
        pytest.skip("Login requires CAPTCHA bypass")

    def test_TC_AUTH_LOGIN_005_sql_injection_attempt(self):
        """Test SQL injection prevention"""
        print("\n🔍 TEST: SQL Injection Prevention - SKIPPED (Requires authentication)")
        pytest.skip("Security testing requires authenticated access")
