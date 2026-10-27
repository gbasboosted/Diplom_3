import allure

from locators.feed_locators import FeedLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    @allure.step("Дождаться загрузки ленты заказов")
    def wait_loaded(self):
        self.visible(FeedLocators.HEADING)
        self.number(FeedLocators.TOTAL)
        self.number(FeedLocators.TODAY)
        self.visible(FeedLocators.ORDER_CARDS)
        return self

    @allure.step("Прочитать счётчик {metric}")
    def completed_count(self, metric):
        locator = {"total": FeedLocators.TOTAL, "today": FeedLocators.TODAY}[metric]
        return self.number(locator)

    @allure.step("Дождаться увеличения счётчика {metric}")
    def wait_count_increased(self, metric, before):
        self.wait_until(lambda: self.completed_count(metric) > before)
        return self.completed_count(metric)

    @allure.step("Дождаться своего заказа в ленте")
    def wait_order_in_feed(self, number):
        return self.wait_text_match(FeedLocators.ORDER_CARDS, rf"#\s*0*{number}\b")

    @allure.step("Начать наблюдение за номерами в разделе «В работе»")
    def observe_in_progress(self):
        self.observe_list_numbers(FeedLocators.IN_PROGRESS)

    @allure.step("Проверить появление номера своего заказа в разделе «В работе»")
    def wait_order_in_progress(self, number):
        return self.wait_observed_number(number)

    @allure.step("Открыть ленту в отдельной вкладке")
    def open_observer_tab(self):
        handle = self.open_tab("/feed")
        self.wait_loaded()
        return handle
