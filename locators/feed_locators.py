from selenium.webdriver.common.by import By


class FeedLocators:
    HEADING = (By.XPATH, "//h1[normalize-space()='Лента заказов']")
    TOTAL = (
        By.XPATH,
        "//*[self::h2 or self::h3 or self::p]"
        "[starts-with(normalize-space(), 'Выполнено за вс')]/following-sibling::p[1]",
    )
    TODAY = (
        By.XPATH,
        "//*[self::h2 or self::h3 or self::p]"
        "[starts-with(normalize-space(), 'Выполнено за сегодня')]/following-sibling::p[1]",
    )
    IN_PROGRESS = (
        By.XPATH,
        "//*[self::h2 or self::h3 or self::p]"
        "[translate(normalize-space(), ':', '')='В работе']/following-sibling::ul[1]",
    )
    ORDER_CARDS = (By.CSS_SELECTOR, "a[href^='/feed/']")
