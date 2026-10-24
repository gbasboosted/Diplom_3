import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from locators.constructor_locators import ConstructorLocators
from pages.base_page import BasePage
from pages.modal import Modal


class ConstructorPage(BasePage):
    def _ingredient_card(self, locator):
        card = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
        return self.visible(locator)

    def wait_loaded(self):
        self.visible(ConstructorLocators.HEADING)
        self.visible(ConstructorLocators.FIRST_BUN)
        return self

    @allure.step("Прочитать название первой булочки")
    def first_bun_name(self):
        return self.visible(ConstructorLocators.FIRST_BUN).find_element(
            *ConstructorLocators.INGREDIENT_NAME
        ).text

    @allure.step("Открыть детали первой булочки")
    def open_first_bun_details(self):
        self.click(ConstructorLocators.FIRST_BUN)
        modal = Modal(self.driver)
        modal.root()
        return modal

    def filling_count(self):
        card = self._ingredient_card(ConstructorLocators.FIRST_FILLING)
        counters = card.find_elements(*ConstructorLocators.COUNTER)
        return int(counters[0].text) if counters else 0

    @allure.step("Перетащить ингредиент в конструктор")
    def add_ingredient(self, locator):
        source = self._ingredient_card(locator)
        target = self.visible(ConstructorLocators.DROP_AREA)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    @allure.step("Добавить первую начинку в заказ")
    def add_first_filling(self):
        self.add_ingredient(ConstructorLocators.FIRST_FILLING)

    def wait_filling_count(self, expected):
        self.wait.until(lambda _: self.filling_count() == expected)
        return self.filling_count()

    @allure.step("Собрать бургер из булочки и начинки")
    def build_burger(self):
        self.add_ingredient(ConstructorLocators.FIRST_BUN)
        self.add_first_filling()
        self.wait_filling_count(1)

    @allure.step("Оформить заказ через интерфейс")
    def place_order(self):
        self.click(ConstructorLocators.PLACE_ORDER)
        modal = Modal(self.driver)
        number = modal.order_number()
        modal.close()
        return number

    def is_authenticated(self):
        return self.visible(ConstructorLocators.PLACE_ORDER).is_enabled()
