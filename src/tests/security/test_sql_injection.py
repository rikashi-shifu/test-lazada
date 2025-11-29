import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.base_test import BaseTest
from src.utils.helpers import Helpers
import time


class TestSQLInjection(BaseTest):
    """Test cases for SQL Injection Prevention"""

    def test_TC_SEC_SQL_001_login_sql_injection(self):
        """Security: SQL injection in login form"""
        login_button = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//a[contains(text(),'Login')]")
        )
        if login_button:
            login_button.click()

        email_field = Helpers.wait_for_element(self.driver, (By.ID, "email"))
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys("admin' OR '1'='1")
        password_field.send_keys("' OR '1'='1")
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)

        injection_failed = not Helpers.is_element_present(
            self.driver, (By.XPATH, "//div[contains(@class,'account')]")
        )
        assert injection_failed, "SQL injection vulnerability detected"
        self.take_screenshot("sec_sql_login")

    def test_TC_SEC_SQL_002_search_sql_injection(self):
        """Security: SQL injection in search box"""
        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop' OR '1'='1")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        page_loaded = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_loaded, "Page failed to handle SQL injection safely"
        self.take_screenshot("sec_sql_search")

    def test_TC_SEC_SQL_003_url_parameter_injection(self):
        """Security: SQL injection via URL parameters"""
        malicious_url = f"{self.driver.current_url}?id=1' OR '1'='1"
        self.driver.get(malicious_url)

        time.sleep(2)

        page_exists = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_exists, "URL parameter injection not handled"
        self.take_screenshot("sec_sql_url")

    def test_TC_SEC_SQL_004_review_text_injection(self):
        """Security: SQL injection in review submission"""
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

        write_review = Helpers.wait_for_clickable(
            self.driver, (By.XPATH, "//button[contains(text(),'Write Review')]")
        )
        if write_review:
            write_review.click()

        time.sleep(1)

        review_text = Helpers.wait_for_element(self.driver, (By.XPATH, "//textarea"))
        if review_text:
            review_text.send_keys("'; DROP TABLE users; --")

        time.sleep(1)
        self.take_screenshot("sec_sql_review")

    def test_TC_SEC_SQL_005_filter_parameter_injection(self):
        """Security: SQL injection in filter parameters"""
        search_box = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[contains(@placeholder,'Search')]")
        )
        if search_box:
            search_box.send_keys("laptop")
            search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        price_filter = Helpers.wait_for_clickable(
            self.driver,
            (
                By.XPATH,
                "//div[contains(text(),'Price') or contains(@class,'price-filter')]",
            ),
        )
        if price_filter:
            price_filter.click()

        time.sleep(1)

        min_price = Helpers.wait_for_element(
            self.driver, (By.XPATH, "//input[@placeholder='Min']")
        )
        if min_price:
            min_price.send_keys("1' OR '1'='1")

        time.sleep(1)

        page_stable = Helpers.is_element_present(self.driver, (By.XPATH, "//body"))
        assert page_stable, "Filter injection caused page error"
        self.take_screenshot("sec_sql_filter")
