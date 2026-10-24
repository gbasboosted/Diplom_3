import re

import allure

from locators.feed_locators import FeedLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    def wait_loaded(self):
        self.visible(FeedLocators.HEADING)
        self.wait.until(lambda _: re.sub(r"\s", "", self.visible(FeedLocators.TOTAL).text).isdigit())
        self.wait.until(lambda _: re.sub(r"\s", "", self.visible(FeedLocators.TODAY).text).isdigit())
        self.visible(FeedLocators.ORDER_CARDS)
        return self

    @allure.step("Прочитать счётчик {metric}")
    def completed_count(self, metric):
        locator = {"total": FeedLocators.TOTAL, "today": FeedLocators.TODAY}[metric]
        return int(re.sub(r"\s", "", self.visible(locator).text))

    @allure.step("Дождаться увеличения счётчика {metric}")
    def wait_count_increased(self, metric, before):
        self.wait.until(lambda _: self.completed_count(metric) > before)
        return self.completed_count(metric)

    @allure.step("Дождаться своего заказа в ленте")
    def wait_order_in_feed(self, number):
        def found(driver):
            for card in driver.find_elements(*FeedLocators.ORDER_CARDS):
                match = re.search(r"#\s*(\d+)", card.text)
                if match and int(match.group(1)) == number:
                    return True
            return False

        self.wait.until(found)
        return True

    @allure.step("Начать наблюдение за номерами в разделе «В работе»")
    def observe_in_progress(self):
        self.visible(FeedLocators.IN_PROGRESS)
        # Наблюдаем реальный DOM, чтобы не пропустить кратковременное появление
        # заказа, пока другая вкладка ждёт окно подтверждения. Данные UI не меняем.
        self.driver.execute_script(r"""
            window.__stellarInProgressObserver?.disconnect();
            window.__stellarSeenOrders = [];
            const xpath = arguments[0];
            const capture = () => {
                const list = document.evaluate(xpath, document, null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
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
        """, FeedLocators.IN_PROGRESS[1])

    @allure.step("Проверить появление номера своего заказа в разделе «В работе»")
    def wait_order_in_progress(self, number):
        self.wait.until(lambda _: self.driver.execute_script(
            "return (window.__stellarSeenOrders || []).includes(arguments[0]);", number,
        ))
        return True

    @allure.step("Открыть ленту в отдельной вкладке")
    def open_observer_tab(self):
        self.driver.switch_to.new_window("tab")
        self.open("/feed")
        self.wait_loaded()
        return self.driver.current_window_handle
