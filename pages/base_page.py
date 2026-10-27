import re
from contextlib import suppress
from urllib.parse import urlparse

import allure
from selenium.common.exceptions import (
    NoSuchElementException, StaleElementReferenceException, TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, WAIT_TIMEOUT
from helpers import SecretText
from locators.header_locators import HeaderLocators
from locators.modal_locators import ModalLocators


class BasePage:
    @allure.step("Создать объект страницы")
    def __init__(self, driver):
        self._driver = driver

    @allure.step("Дождаться выполнения условия")
    def wait_until(self, condition, timeout=WAIT_TIMEOUT):
        return WebDriverWait(
            self._driver, timeout,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        ).until(lambda _: condition())

    @allure.step("Найти элементы {locator} в заданной области")
    def _elements(self, locator, parent=None):
        scope = self._driver
        if parent is not None:
            scope = next((item for item in self._driver.find_elements(*parent)
                          if item.is_displayed()), None)
            if scope is None:
                return []
        return scope.find_elements(*locator)

    @allure.step("Открыть страницу {path}")
    def open(self, path="/"):
        try:
            self._driver.get(f"{BASE_URL}{path}")
        except TimeoutException:
            with suppress(WebDriverException):
                self._driver.execute_script("window.stop();")
            raise
        return self

    @allure.step("Дождаться видимого элемента {locator}")
    def visible(self, locator, parent=None):
        return self.wait_until(lambda: next(
            (item for item in self._elements(locator, parent) if item.is_displayed()), False,
        ))

    @allure.step("Проверить видимость элемента {locator}")
    def is_visible(self, locator, parent=None):
        return any(item.is_displayed() for item in self._elements(locator, parent))

    @allure.step("Нажать элемент {locator}")
    def click(self, locator, parent=None, wait_for_overlays=True):
        if wait_for_overlays:
            self.wait_overlays_closed()
        element = self.wait_until(lambda: EC.element_to_be_clickable(
            self.visible(locator, parent)
        )(self._driver))
        element.click()

    @allure.step("Заполнить поле {locator}")
    def fill(self, locator, value):
        text = value.value if isinstance(value, SecretText) else value
        element = self.visible(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Прочитать текст элемента {locator}")
    def text(self, locator, parent=None):
        return self.visible(locator, parent).text

    @allure.step("Дождаться числа в элементе {locator}")
    def number(self, locator, parent=None, excluded=(), ready=None, timeout=WAIT_TIMEOUT):
        def read_number():
            if ready is not None and not self.is_visible(ready, parent):
                return False
            for item in self._elements(locator, parent):
                text = re.sub(r"\s", "", item.text)
                if item.is_displayed() and text.isdigit() and int(text) not in excluded:
                    # Кортеж позволяет WebDriverWait принять число 0 как результат.
                    return (int(text),)
            return False

        return self.wait_until(read_number, timeout)[0]

    @allure.step("Проверить доступность элемента {locator}")
    def is_enabled(self, locator):
        return self.visible(locator).is_enabled()

    @allure.step("Прокрутить страницу к элементу {locator}")
    def scroll_to(self, locator):
        element = self.visible(locator)
        self._driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element,
        )

    @allure.step("Дождаться исчезновения загрузочных подложек")
    def wait_overlays_closed(self):
        self.wait_until(lambda: not self.is_visible(ModalLocators.OVERLAYS))

    @allure.step("Получить путь текущей страницы")
    def path(self):
        return urlparse(self._driver.current_url).path

    @allure.step("Дождаться перехода на {path}")
    def wait_path(self, path):
        self.wait_until(lambda: self.path().rstrip("/") == path.rstrip("/"))

    @allure.step("Нажать «Конструктор» в шапке")
    def click_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR)
        self.wait_path("/")

    @allure.step("Нажать «Лента заказов» в шапке")
    def click_feed(self):
        self.click(HeaderLocators.FEED)
        self.wait_path("/feed")

    @allure.step("Перетащить элемент {source_locator} в {target_locator}")
    def drag_and_drop(self, source_locator, target_locator):
        self.wait_overlays_closed()
        self.scroll_to(source_locator)
        source = self.visible(source_locator)
        target = self.visible(target_locator)
        if self._driver.capabilities["browserName"] == "firefox":
            # Gecko требует DOM DragEvent с общим DataTransfer для HTML5 drop.
            self._driver.execute_script("""
                const [source, target] = arguments;
                const dataTransfer = new DataTransfer();
                const rect = target.getBoundingClientRect();
                const options = {
                    bubbles: true, cancelable: true, dataTransfer,
                    clientX: rect.x + rect.width / 2,
                    clientY: rect.y + rect.height / 2,
                };
                source.dispatchEvent(new DragEvent('dragstart', options));
                target.dispatchEvent(new DragEvent('dragenter', options));
                target.dispatchEvent(new DragEvent('dragover', options));
                target.dispatchEvent(new DragEvent('drop', options));
                source.dispatchEvent(new DragEvent('dragend', options));
            """, source, target)
        else:
            # Отдельный начальный сдвиг запускает dragstart до движения к корзине.
            (ActionChains(self._driver)
             .move_to_element(source)
             .click_and_hold()
             .pause(0.2)
             .move_by_offset(10, 0)
             .pause(0.2)
             .move_to_element(target)
             .pause(0.2)
             .release()
             .perform())

    @allure.step("Получить идентификатор текущей вкладки")
    def current_tab(self):
        return self._driver.current_window_handle

    @allure.step("Открыть новую вкладку со страницей {path}")
    def open_tab(self, path):
        self._driver.switch_to.new_window("tab")
        self.open(path)
        return self.current_tab()

    @allure.step("Переключиться на вкладку {handle}")
    def switch_tab(self, handle):
        self._driver.switch_to.window(handle)

    @allure.step("Дождаться текста {pattern} в элементах {locator}")
    def wait_text_match(self, locator, pattern):
        self.wait_until(lambda: any(re.search(pattern, item.text)
                                   for item in self._elements(locator)))
        return True

    @allure.step("Наблюдать за числами в списке {locator}")
    def observe_list_numbers(self, locator):
        self.visible(locator)
        # Наблюдатель только читает DOM; собственные данные приложения не меняет.
        self._driver.execute_script(r"""
            window.__stellarInProgressObserver?.disconnect();
            window.__stellarSeenOrders = [];
            const [strategy, selector] = arguments;
            const capture = () => {
                const list = strategy === 'xpath'
                    ? document.evaluate(selector, document, null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
                    : document.querySelector(selector);
                const numbers = Array.from(list?.querySelectorAll('li') || [])
                    .flatMap(item => item.textContent.match(/\d+/g) || []);
                for (const number of numbers) {
                    const value = Number(number);
                    if (!window.__stellarSeenOrders.includes(value)) {
                        window.__stellarSeenOrders.push(value);
                    }
                }
            };
            window.__stellarInProgressObserver = new MutationObserver(capture);
            window.__stellarInProgressObserver.observe(document.body,
                {subtree: true, childList: true, characterData: true});
            capture();
        """, *locator)

    @allure.step("Дождаться появления числа {number} в наблюдаемом списке")
    def wait_observed_number(self, number):
        self.wait_until(lambda: self._driver.execute_script(
            "return (window.__stellarSeenOrders || []).includes(arguments[0]);", number,
        ))
        return True

    @allure.step("Приложить диагностику страницы при ошибке")
    def attach_failure_diagnostics(self):
        allure.attach(
            self._driver.get_screenshot_as_png(), "Снимок при ошибке",
            allure.attachment_type.PNG,
        )
        html = self._driver.execute_script("""
            const copy = document.documentElement.cloneNode(true);
            copy.querySelectorAll('input').forEach(input => input.removeAttribute('value'));
            copy.querySelectorAll('script').forEach(script => script.remove());
            return copy.outerHTML;
        """)
        allure.attach(html, "DOM при ошибке", allure.attachment_type.HTML)
        allure.attach(self._driver.current_url, "URL при ошибке", allure.attachment_type.TEXT)
