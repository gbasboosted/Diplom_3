import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from config import PAGE_LOAD_TIMEOUT


def build_driver(browser, headed=False):
    if browser == "chrome":
        options = ChromeOptions()
        if not headed:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-dev-shm-usage")
        if os.getenv("CHROME_BINARY"):
            options.binary_location = os.environ["CHROME_BINARY"]
        path = os.getenv("CHROMEDRIVER_PATH")
        service = ChromeService(executable_path=path) if path else ChromeService()
        driver = webdriver.Chrome(options=options, service=service)
    else:
        options = FirefoxOptions()
        if not headed:
            options.add_argument("-headless")
        if os.getenv("FIREFOX_BINARY"):
            options.binary_location = os.environ["FIREFOX_BINARY"]
        path = os.getenv("GECKODRIVER_PATH")
        service = FirefoxService(executable_path=path) if path else FirefoxService()
        driver = webdriver.Firefox(options=options, service=service)
    driver.implicitly_wait(0)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.set_window_size(1440, 1000)
    return driver
