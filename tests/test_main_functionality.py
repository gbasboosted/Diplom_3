import allure

from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from pages.modal import Modal


@allure.epic("Stellar Burgers UI")
@allure.feature("Основная функциональность")
class TestMainFunctionality:
    @allure.title("Переход по клику на «Конструктор»")
    def test_click_constructor_opens_constructor(self, driver):
        feed = FeedPage(driver).open("/feed").wait_loaded()

        feed.click_constructor()

        constructor = ConstructorPage(driver).wait_loaded()
        assert constructor.path() == "/"

    @allure.title("Переход по клику на «Лента заказов»")
    def test_click_feed_opens_order_feed(self, driver):
        constructor = ConstructorPage(driver).open().wait_loaded()

        constructor.click_feed()

        feed = FeedPage(driver).wait_loaded()
        assert feed.path().rstrip("/") == "/feed"

    @allure.title("Клик по ингредиенту открывает окно с его деталями")
    def test_click_ingredient_opens_details(self, driver):
        constructor = ConstructorPage(driver).open().wait_loaded()
        expected_name = constructor.bun_name()

        constructor.open_bun_details()
        modal = Modal(driver)

        assert modal.ingredient_title() == "Детали ингредиента"
        assert modal.ingredient_name() == expected_name

    @allure.title("Окно с деталями ингредиента закрывается крестиком")
    def test_ingredient_details_close_by_cross(self, driver):
        constructor = ConstructorPage(driver).open().wait_loaded()
        constructor.open_bun_details()
        modal = Modal(driver)
        modal.root()
        assert modal.is_open()

        modal.close()

        constructor.wait_loaded()
        assert not modal.is_open()

    @allure.title("Добавление начинки увеличивает её счётчик на единицу")
    def test_adding_ingredient_increases_counter(self, driver):
        constructor = ConstructorPage(driver).open().wait_loaded()
        before = constructor.filling_count()

        constructor.add_filling()

        assert constructor.wait_filling_count(before + 1) == before + 1
