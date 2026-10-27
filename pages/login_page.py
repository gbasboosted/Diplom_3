import allure

from locators.login_locators import LoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    @allure.step("Войти под тестовым пользователем через форму")
    def login(self, user):
        self.open("/login")
        self.fill(LoginLocators.EMAIL, user.email)
        self.fill(LoginLocators.PASSWORD, user.password)
        self.click(LoginLocators.SUBMIT)
        self.wait_path("/")
