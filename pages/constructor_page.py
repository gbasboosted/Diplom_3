import allure

from locators.constructor_locators import ConstructorLocators
from pages.base_page import BasePage


class ConstructorPage(BasePage):
    @allure.step("Дождаться загрузки конструктора")
    def wait_loaded(self):
        self.visible(ConstructorLocators.HEADING)
        self.visible(ConstructorLocators.BUN)
        return self

    @allure.step("Прочитать название выбранной булочки")
    def bun_name(self):
        return self.text(ConstructorLocators.INGREDIENT_NAME, parent=ConstructorLocators.BUN)

    @allure.step("Открыть детали выбранной булочки")
    def open_bun_details(self):
        self.click(ConstructorLocators.BUN)

    @allure.step("Прочитать счётчик выбранной начинки")
    def filling_count(self):
        self.scroll_to(ConstructorLocators.FILLING)
        return self.number(ConstructorLocators.COUNTER, parent=ConstructorLocators.FILLING)

    @allure.step("Перетащить ингредиент в конструктор")
    def add_ingredient(self, locator):
        self.drag_and_drop(locator, ConstructorLocators.DROP_AREA)

    @allure.step("Добавить выбранную начинку в заказ")
    def add_filling(self):
        self.add_ingredient(ConstructorLocators.FILLING)

    @allure.step("Дождаться счётчика начинки {expected}")
    def wait_filling_count(self, expected):
        self.wait_until(lambda: self.filling_count() == expected)
        return self.filling_count()

    @allure.step("Собрать бургер из булочки и начинки")
    def build_burger(self):
        self.add_ingredient(ConstructorLocators.BUN)
        self.add_filling()
        self.wait_filling_count(1)

    @allure.step("Нажать «Оформить заказ»")
    def place_order(self):
        self.click(ConstructorLocators.PLACE_ORDER)

    @allure.step("Проверить доступность оформления заказа")
    def is_authenticated(self):
        return self.is_enabled(ConstructorLocators.PLACE_ORDER)
