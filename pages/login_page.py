import allure

from locators.login_locators import LoginLocators
from pages.base_page import BasePage
from pages.constructor_page import ConstructorPage


class LoginPage(BasePage):
    def login(self, user):
        # Контекст шага не сериализует аргумент user с паролем в Allure.
        with allure.step("Войти под тестовым пользователем через форму"):
            self.open("/login")
            self.visible(LoginLocators.EMAIL).send_keys(user["email"])
            self.visible(LoginLocators.PASSWORD).send_keys(user["password"])
            self.click(LoginLocators.SUBMIT)
            self.wait.until(lambda _: self.path() == "/")
            page = ConstructorPage(self.driver).wait_loaded()
            assert page.is_authenticated()
            return page
