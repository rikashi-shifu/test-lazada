from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time


class Helpers:
    @staticmethod
    def wait_for_element(driver, locator, timeout=20):
        """Wait for element to be present with retry logic"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            return None

    @staticmethod
    def wait_for_clickable(driver, locator, timeout=20):
        """Wait for element to be clickable with retry logic"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                element = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                return element
            except (TimeoutException, StaleElementReferenceException):
                if attempt == max_attempts - 1:
                    return None
                time.sleep(1)
        return None

    @staticmethod
    def is_element_present(driver, locator):
        """Check if element is present"""
        try:
            driver.find_element(*locator)
            return True
        except:
            return False

    @staticmethod
    def close_popups(driver):
        """Close any popups or overlays that might be blocking elements"""
        popup_selectors = [
            # Lazada's common popup close buttons
            "//button[contains(@class, 'close')]",
            "//div[contains(@class, 'close')]",
            "//span[contains(@class, 'close')]",
            "//button[@aria-label='Close']",
            "//div[@class='J_MIDDLEWARE_FRAME_WIDGET']//button",
            # X buttons
            "//button[text()='×']",
            "//span[text()='×']",
        ]

        for selector in popup_selectors:
            try:
                close_btn = driver.find_element(By.XPATH, selector)
                if close_btn.is_displayed():
                    close_btn.click()
                    time.sleep(0.5)
                    print("✓ Closed popup")
            except:
                continue

    @staticmethod
    def scroll_to_element(driver, element):
        """Scroll element into view"""
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                element,
            )
            time.sleep(0.5)
        except:
            pass

    @staticmethod
    def click_with_js(driver, element):
        """Click element using JavaScript (bypasses overlays)"""
        try:
            driver.execute_script("arguments[0].click();", element)
            return True
        except:
            return False

    @staticmethod
    def retry_find_element(driver, locator, max_attempts=3):
        """Retry finding element if it becomes stale"""
        for attempt in range(max_attempts):
            try:
                element = driver.find_element(*locator)
                # Test if element is still valid
                element.is_displayed()
                return element
            except StaleElementReferenceException:
                if attempt == max_attempts - 1:
                    return None
                time.sleep(1)
        return None
