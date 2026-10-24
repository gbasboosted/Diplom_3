import allure
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait

from config import ORDER_TIMEOUT
from locators.modal_locators import ModalLocators
from pages.base_page import BasePage


class Modal(BasePage):
    def _visible_root(self, driver):
        return next(
            (item for item in driver.find_elements(*ModalLocators.ROOT) if item.is_displayed()),
            False,
        )

    def root(self):
        return self.wait.until(self._visible_root)

    @allure.step("Прочитать заголовок окна ингредиента")
    def ingredient_title(self):
        return self.root().find_element(*ModalLocators.TITLE).text

    @allure.step("Прочитать название ингредиента в окне")
    def ingredient_name(self):
        return self.root().find_element(*ModalLocators.INGREDIENT_NAME).text

    @allure.step("Закрыть всплывающее окно крестиком")
    def close(self):
        self.root().find_element(*ModalLocators.CLOSE).click()
        self.wait.until(lambda _: not self.is_open())

    def is_open(self):
        return any(item.is_displayed() for item in self.driver.find_elements(*ModalLocators.ROOT))

    @allure.step("Дождаться номера оформленного заказа")
    def order_number(self):
        def confirmed_number(_):
            try:
                modal = self._visible_root(self.driver)
                if not modal:
                    return False
                if not modal.find_element(*ModalLocators.ORDER_CONFIRMED).is_displayed():
                    return False
                text = modal.find_element(*ModalLocators.ORDER_NUMBER).text.strip()
                # 9999 — временное значение в окне до получения номера от сервера.
                return int(text) if text.isdigit() and int(text) not in (0, 9999) else False
            except NoSuchElementException:
                return False

        return WebDriverWait(
            self.driver, ORDER_TIMEOUT, ignored_exceptions=(StaleElementReferenceException,),
        ).until(confirmed_number)
