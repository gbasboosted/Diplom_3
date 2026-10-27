from selenium.webdriver.common.by import By


class ConstructorLocators:
    HEADING = (By.XPATH, "//h1[normalize-space()='Соберите бургер']")
    BUN = (
        By.XPATH,
        "//a[starts-with(@href, '/ingredient/') and .//img[@alt='Краторная булка N-200i']]",
    )
    FILLING = (
        By.XPATH,
        "//a[starts-with(@href, '/ingredient/') and "
        ".//img[@alt='Мясо бессмертных моллюсков Protostomia']]",
    )
    INGREDIENT_NAME = (By.CSS_SELECTOR, "p[class*='BurgerIngredient_ingredient__text']")
    COUNTER = (By.CSS_SELECTOR, "p[class*='counter_counter__num']")
    DROP_AREA = (
        By.XPATH,
        "//section[.//button[normalize-space()='Оформить заказ' or "
        "normalize-space()='Войти в аккаунт']]"
        "[not(.//section[.//button[normalize-space()='Оформить заказ' or "
        "normalize-space()='Войти в аккаунт']])]",
    )
    PLACE_ORDER = (By.XPATH, "//button[normalize-space()='Оформить заказ']")
