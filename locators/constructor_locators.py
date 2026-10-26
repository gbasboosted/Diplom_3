from selenium.webdriver.common.by import By


class ConstructorLocators:
    HEADING = (By.XPATH, "//h1[normalize-space()='Соберите бургер']")
    FIRST_BUN = (By.XPATH, "(//a[starts-with(@href, '/ingredient/')])[1]")
    FIRST_FILLING = (
        By.XPATH,
        "(//h2[normalize-space()='Начинки']/following-sibling::*[1]"
        "//a[starts-with(@href, '/ingredient/')])[1]",
    )
    INGREDIENT_NAME = (By.CSS_SELECTOR, "p[class*='BurgerIngredient_ingredient__text']")
    COUNTER = (By.CSS_SELECTOR, "[class*='counter_counter__']")
    DROP_AREA = (
        By.XPATH,
        "//section[.//button[normalize-space()='Оформить заказ' or "
        "normalize-space()='Войти в аккаунт']]"
        "[not(.//section[.//button[normalize-space()='Оформить заказ' or "
        "normalize-space()='Войти в аккаунт']])]",
    )
    PLACE_ORDER = (By.XPATH, "//button[normalize-space()='Оформить заказ']")
