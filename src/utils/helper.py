from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Helpers:
    @staticmethod
    def wait_for_element(driver, locator, timeout=20):
        """Wait for element to be present"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            return None

    @staticmethod
    def wait_for_clickable(driver, locator, timeout=20):
        """Wait for element to be clickable"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            return None

    @staticmethod
    def is_element_present(driver, locator):
        """Check if element is present"""
        try:
            driver.find_element(*locator)
            return True
        except:
            return False
