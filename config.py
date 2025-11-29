from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = "https://www.lazada.com.my"
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30

    # Test credentials
    TEST_EMAIL = os.getenv("TEST_EMAIL", "testuser@example.com")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "TestPass123!")

    # Browser settings
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chrome")

    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        return driver
