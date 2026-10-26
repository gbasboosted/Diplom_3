from selenium.webdriver.common.by import By


class LoginLocators:
    EMAIL = (By.CSS_SELECTOR, "form input[type='text']")
    PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT = (By.XPATH, "//button[normalize-space()='Войти']")
