import allure

from config import ORDER_TIMEOUT
from locators.modal_locators import ModalLocators
from pages.base_page import BasePage


class Modal(BasePage):
    @allure.step("Дождаться видимого всплывающего окна")
    def root(self):
        return self.visible(ModalLocators.ROOT)

    @allure.step("Прочитать заголовок окна ингредиента")
    def ingredient_title(self):
        return self.text(ModalLocators.TITLE, parent=ModalLocators.ROOT)

    @allure.step("Прочитать название ингредиента в окне")
    def ingredient_name(self):
        return self.text(ModalLocators.INGREDIENT_NAME, parent=ModalLocators.ROOT)

    @allure.step("Закрыть всплывающее окно крестиком")
    def close(self):
        self.click(ModalLocators.CLOSE, parent=ModalLocators.ROOT, wait_for_overlays=False)
        self.wait_until(lambda: not self.is_open())

    @allure.step("Проверить, открыто ли всплывающее окно")
    def is_open(self):
        return self.is_visible(ModalLocators.ROOT)

    @allure.step("Дождаться номера оформленного заказа")
    def order_number(self):
        return self.number(
            ModalLocators.ORDER_NUMBER, parent=ModalLocators.ROOT,
            excluded=(0, 9999), ready=ModalLocators.ORDER_CONFIRMED, timeout=ORDER_TIMEOUT,
        )
