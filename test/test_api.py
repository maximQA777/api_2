from selene import browser, have, be
from allure_commons._allure import step
from qa_api_demoSHOP.demoshop_api import BaseApiClient
from test.conftest import BASE_URL
from time import sleep

LOGIN = "alabai.vfrcbv2001@mail.ru"
PASSWORD = "Maks123"


def test_login_and_logout_shop():
        login_url = '/login'
        logout_url = '/logout'

        # 1. Авторизация через API
        with step("Авторизация через API"):
            data = {"Email": LOGIN, "Password": PASSWORD, "RememberMe": False}  # Данные для авторизации
            login_result = BaseApiClient.api_request(login_url, method="POST", data=data, allow_redirects=False)
            assert login_result.status_code == 302, f"Ожидался код 302, но получен {login_result.status_code}"
            auth_cookie = login_result.cookies.get("NOPCOMMERCE.AUTH")

        # 2. Проверка авторизации в UI
        with step("Проверка авторизации в UI"):
            browser.open(BASE_URL)
            browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": auth_cookie})
            browser.open(BASE_URL)
            browser.element(".account").should(have.text(LOGIN))

        # 3. Выход из аккаунта через API
        with step("Выход из аккаунта через API"):
            logout_result = BaseApiClient.api_request(logout_url,
                                                      method="GET",
                                                      allow_redirects=False)
            assert logout_result.status_code == 302, f"Ожидался код 302 при логауте, но получен {logout_result.status_code}"

        # 4. Проверка выхода из аккаунта в UI
        with step("Проверить логаут в браузере"):
            browser.driver.delete_cookie("NOPCOMMERCE.AUTH")
            browser.open(BASE_URL)
            browser.element(".ico-login").should(be.visible)


def test_adding_goods_to_the_cart():
    add_url = "/addproducttocart/catalog/31/1/1"
    cart_url = "/cart"
    cookie_name = "Nop.customer"

    with step("Добавление товара в корзину через API"):
        result = BaseApiClient.api_request(add_url, method="POST")
        cookie = result.cookies.get(cookie_name)
        assert cookie, "Не получена кука после добавления товара"

    with step("Открытие корзины с установленной кукой"):
        browser.open(BASE_URL)
        browser.driver.add_cookie({"name": cookie_name, "value": cookie})
        browser.open(BASE_URL + cart_url)

    with step("Проверка содержимого корзины"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.element(".product-price.order-total").should(have.text("1590.00"))


def test_increase_quantity_goods_to_the_cart():
    add_url = "/addproducttocart/catalog/31/1/1"
    cart_url = "/cart"
    cookie_name = "Nop.customer"

    with step("Добавление товара в корзину через API"):
        result = BaseApiClient.api_request(add_url, method="POST")
        cookie = result.cookies.get(cookie_name)
        assert cookie, "Не получена кука после первого добавления"

    with step("Повторное добавление товара через API для увеличения количества"):
        BaseApiClient.api_request(add_url, method="POST", cookies={cookie_name: cookie})

    with step("Открытие корзины с кукой"):
        browser.open(BASE_URL)
        browser.driver.add_cookie({"name": cookie_name, "value": cookie})
        browser.open(BASE_URL + cart_url)

    with step("Проверка количества товаров и цены"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.element(".product-price.order-total").should(have.text("3180.00"))


def test_adding_several_goods_to_the_cart():
    laptop_url = "/addproducttocart/catalog/31/1/1"
    customizable_url = "/addproducttocart/details/72/1"
    cart_url = "/cart"
    cookie_name = "Nop.customer"

    with step("Добавление первого товара через API"):
        result = BaseApiClient.api_request(laptop_url, method="POST")
        cookie = result.cookies.get(cookie_name)
        assert cookie, "Не получена кука после первого добавления"

    with step("Добавление настраиваемого товара через API"):
        BaseApiClient.api_request(
            customizable_url,
            method="POST",
            data={
                "product_attribute_72_5_18": 3,
                "product_attribute_72_6_19": 54,
                "product_attribute_72_3_20": 57,
                "addtocart_72.EnteredQuantity": 1,
            },
            cookies={cookie_name: cookie}
        )

    with step("Открытие корзины с кукой"):
        browser.open(BASE_URL)
        browser.driver.add_cookie({"name": cookie_name, "value": cookie})
        browser.open(BASE_URL + cart_url)

    with step("Проверка двух товаров в корзине"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.all(".attributes").should(have.texts("Processor: 2X\nRAM: 2 GB\nHDD: 320 GB"))
        browser.element(".product-price.order-total").should(have.text("2390.00"))