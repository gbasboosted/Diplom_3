from selenium.webdriver.common.by import By


class ModalLocators:
    ROOT = (By.CSS_SELECTOR, "[class*='Modal_modal__'], [class*='modal_modal__']")
    TITLE = (
        By.XPATH,
        ".//*[self::h2 or self::h3][normalize-space()='Детали ингредиента']",
    )
    INGREDIENT_NAME = (By.CSS_SELECTOR, ".text_type_main-medium")
    CLOSE = (
        By.XPATH,
        ".//button[@aria-label='Закрыть' or contains(@class, 'close') "
        "or contains(@class, 'Close') or .//*[local-name()='svg']][1]",
    )
    ORDER_NUMBER = (
        By.XPATH,
        ".//*[self::h2 or self::p][contains(@class, 'text_type_digits-large')]",
    )
    ORDER_CONFIRMED = (
        By.XPATH, ".//p[normalize-space()='Ваш заказ начали готовить']",
    )
