from contextlib import suppress
from urllib.parse import urlparse

import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, WAIT_TIMEOUT
from locators.header_locators import HeaderLocators


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, WAIT_TIMEOUT, ignored_exceptions=(StaleElementReferenceException,),
        )

    @allure.step("Открыть страницу {path}")
    def open(self, path="/"):
        try:
            self.driver.get(f"{BASE_URL}{path}")
        except TimeoutException:
            with suppress(WebDriverException):
                self.driver.execute_script("window.stop();")
            raise
        return self

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def path(self):
        return urlparse(self.driver.current_url).path

    @allure.step("Нажать «Конструктор» в шапке")
    def click_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR)
        self.wait.until(lambda _: self.path() == "/")

    @allure.step("Нажать «Лента заказов» в шапке")
    def click_feed(self):
        self.click(HeaderLocators.FEED)
        self.wait.until(lambda _: self.path().rstrip("/") == "/feed")
