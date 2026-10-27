import allure
import pytest

from pages.feed_page import FeedPage
from pages.modal import Modal


@allure.epic("Stellar Burgers UI")
@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Новый заказ увеличивает счётчик {metric}")
    @pytest.mark.parametrize("metric", ["total", "today"], ids=["all-time", "today"])
    def test_new_order_increases_completed_count(self, driver, authenticated_constructor, metric):
        constructor = authenticated_constructor
        constructor.build_burger()
        constructor_tab = constructor.current_tab()
        feed = FeedPage(driver)
        feed_tab = feed.open_observer_tab()
        before = feed.completed_count(metric)

        constructor.switch_tab(constructor_tab)
        constructor.place_order()
        modal = Modal(driver)
        order_number = modal.order_number()
        modal.close()

        feed.switch_tab(feed_tab)
        assert feed.wait_order_in_feed(order_number)
        assert feed.wait_count_increased(metric, before) > before

    @allure.title("Номер оформленного заказа появляется в разделе «В работе»")
    def test_new_order_number_appears_in_progress(self, driver, authenticated_constructor):
        constructor = authenticated_constructor
        constructor.build_burger()
        constructor_tab = constructor.current_tab()
        feed = FeedPage(driver)
        feed_tab = feed.open_observer_tab()
        feed.observe_in_progress()

        constructor.switch_tab(constructor_tab)
        constructor.place_order()
        modal = Modal(driver)
        order_number = modal.order_number()
        modal.close()

        feed.switch_tab(feed_tab)
        assert feed.wait_order_in_progress(order_number)
