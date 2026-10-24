import allure
import pytest

from pages.feed_page import FeedPage


@allure.epic("Stellar Burgers UI")
@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Новый заказ увеличивает счётчик {metric}")
    @pytest.mark.parametrize("metric", ["total", "today"], ids=["all-time", "today"])
    def test_new_order_increases_completed_count(self, driver, authenticated_constructor, metric):
        constructor = authenticated_constructor
        constructor.build_burger()
        constructor_tab = driver.current_window_handle
        feed = FeedPage(driver)
        feed_tab = feed.open_observer_tab()
        before = feed.completed_count(metric)

        driver.switch_to.window(constructor_tab)
        order_number = constructor.place_order()

        driver.switch_to.window(feed_tab)
        assert feed.wait_order_in_feed(order_number)
        assert feed.wait_count_increased(metric, before) > before

    @allure.title("Номер оформленного заказа появляется в разделе «В работе»")
    def test_new_order_number_appears_in_progress(self, driver, authenticated_constructor):
        constructor = authenticated_constructor
        constructor.build_burger()
        constructor_tab = driver.current_window_handle
        feed = FeedPage(driver)
        feed_tab = feed.open_observer_tab()
        feed.observe_in_progress()

        driver.switch_to.window(constructor_tab)
        order_number = constructor.place_order()

        driver.switch_to.window(feed_tab)
        assert feed.wait_order_in_progress(order_number)
