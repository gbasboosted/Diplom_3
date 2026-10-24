import json
import platform
import secrets
from pathlib import Path
from uuid import uuid4

import allure
import pytest
import requests

from browsers import build_driver
from config import API_TIMEOUT, BASE_URL, PAGE_LOAD_TIMEOUT, WAIT_TIMEOUT
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="append", choices=("chrome", "firefox"), default=None,
        help="Браузер; параметр можно повторить. По умолчанию Chrome и Firefox.",
    )
    parser.addoption("--headed", action="store_true", help="Показать окно браузера")


def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
        names = metafunc.config.getoption("browser") or ["chrome", "firefox"]
        metafunc.parametrize("browser_name", list(dict.fromkeys(names)))


@pytest.fixture
def driver(browser_name, pytestconfig):
    allure.dynamic.label("browser", browser_name)
    with allure.step(f"Запустить {browser_name} в отдельном профиле"):
        browser = build_driver(browser_name, pytestconfig.getoption("headed"))
        allure.attach(
            json.dumps({
                key: browser.capabilities.get(key)
                for key in ("browserName", "browserVersion", "platformName")
            }, ensure_ascii=False),
            "Браузер", allure.attachment_type.JSON,
        )
    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def test_user():
    identifier = uuid4().hex
    data = {
        "email": f"stellar-ui-{identifier}@example.com",
        "name": f"UI {identifier[:8]}",
        "password": secrets.token_urlsafe(18),
    }
    session = requests.Session()
    token = None
    try:
        with allure.step("Создать уникального тестового пользователя через API"):
            response = session.post(
                f"{BASE_URL}/api/auth/register", json=data, timeout=API_TIMEOUT,
            )
            assert response.status_code == 200, f"Регистрация: HTTP {response.status_code}"
            body = response.json()
            token = body.get("accessToken")
            assert body["success"] is True
            assert token
        yield data
    finally:
        try:
            if token:
                with allure.step("Удалить созданного тестового пользователя"):
                    response = session.delete(
                        f"{BASE_URL}/api/auth/user",
                        headers={"Authorization": token}, timeout=API_TIMEOUT,
                    )
                    assert response.status_code == 202, f"Удаление: HTTP {response.status_code}"
                    assert response.json()["success"] is True
        finally:
            session.close()


@pytest.fixture
def authenticated_constructor(driver, test_user):
    return LoginPage(driver).login(test_user)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed and report.when in ("setup", "call"):
        browser = item.funcargs.get("driver")
        if browser is not None:
            try:
                allure.attach(browser.get_screenshot_as_png(), "Снимок при ошибке", allure.attachment_type.PNG)
                # Копия DOM без значений полей и скриптов: секреты не попадают в отчёт.
                html = browser.execute_script("""
                    const copy = document.documentElement.cloneNode(true);
                    copy.querySelectorAll('input').forEach(input => input.removeAttribute('value'));
                    copy.querySelectorAll('script').forEach(script => script.remove());
                    return copy.outerHTML;
                """)
                allure.attach(html, "DOM при ошибке", allure.attachment_type.HTML)
                allure.attach(browser.current_url, "URL при ошибке", allure.attachment_type.TEXT)
            except Exception as error:
                allure.attach(type(error).__name__, "Ошибка сохранения диагностики", allure.attachment_type.TEXT)


@pytest.fixture(scope="session", autouse=True)
def allure_environment(pytestconfig):
    yield
    results = pytestconfig.getoption("allure_report_dir")
    if results:
        directory = Path(results)
        directory.mkdir(parents=True, exist_ok=True)
        browsers = pytestconfig.getoption("browser") or ["chrome", "firefox"]
        (directory / "environment.properties").write_text(
            f"Base_URL={BASE_URL}\nPython={platform.python_version()}\n"
            f"OS={platform.system()}\nBrowsers={','.join(browsers)}\n"
            f"Page_load_timeout={PAGE_LOAD_TIMEOUT}\nWait_timeout={WAIT_TIMEOUT}\n",
            encoding="utf-8",
        )
