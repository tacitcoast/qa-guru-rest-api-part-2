import pytest
import requests
from allure import step
from selene.support.conditions import have
from selene.support.shared import browser
from selenium import webdriver


# Настройки для запуска тестов на IOS, в связи с последними изменениями в selene: в binary_location - путь до chrome, чтоб тесты шли в обычный хром
@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.driver_options = webdriver.ChromeOptions()
    browser.config.driver_options.binary_location = ('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')

    yield

    browser.quit()


LOGIN = "example1200@example.com"
PASSWORD = "123456"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"


def test_login():
    with step("Open login page"):
        browser.open("http://demowebshop.tricentis.com/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api():
    with step("Get auth cookie though API"):
        url = API_URL + "/login"
        auth_cookie_name = "NOPCOMMERCE.AUTH"
        payload = {
            'Email': LOGIN,
            "Password": PASSWORD,
            "RememberMe": False
        }
        response = requests.request("POST", url, data=payload, allow_redirects=False)
        cookie = response.cookies.get(auth_cookie_name)

    with step("Open browser with auth cookie"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": auth_cookie_name, "value": cookie})
        browser.open(WEB_URL)

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))