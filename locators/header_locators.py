from selenium.webdriver.common.by import By


class HeaderLocators:
    CONSTRUCTOR = (By.XPATH, "//header//a[.//p[normalize-space()='Конструктор']]")
    FEED = (By.CSS_SELECTOR, "header a[href='/feed']")
