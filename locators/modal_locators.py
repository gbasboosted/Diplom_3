from selenium.webdriver.common.by import By


class ModalLocators:
    OVERLAYS = (By.CSS_SELECTOR, "div[class*='Modal_modal_overlay']")
    ROOT = (By.CSS_SELECTOR, "section[class*='Modal_modal__']")
    TITLE = (
        By.XPATH,
        ".//*[self::h2 or self::h3][normalize-space()='Детали ингредиента']",
    )
    INGREDIENT_NAME = (By.CSS_SELECTOR, ".text_type_main-medium")
    CLOSE = (By.CSS_SELECTOR, "button[type='button'][class*='Modal_modal__close__']")
    ORDER_NUMBER = (
        By.XPATH,
        ".//*[self::h2 or self::p][contains(@class, 'text_type_digits-large')]",
    )
    ORDER_CONFIRMED = (
        By.XPATH, ".//p[normalize-space()='Ваш заказ начали готовить']",
    )
