"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def product_1():
    return Product("notebook", 30, "This is a notebook", 50)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(1000)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        product.buy(100)
        assert product.check_quantity(900)

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)



class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_add_product(self, cart, product):
        cart.add_product(product)
        assert cart.products[product] == 1

        cart.add_product(product, buy_count=2)
        assert cart.products[product] == 3

    def test_cart_remove_one_product(self, cart, product):
        cart.add_product(product, buy_count=2)
        cart.remove_product(product,remove_count=1)
        assert cart.products[product] == 1

    def test_cart_remove_some_products(self, cart, product):
        cart.add_product(product, buy_count=100)
        cart.remove_product(product, remove_count=50)
        assert cart.products[product] == 50

    def test_cart_remove_same_amount_of_products(self, cart, product):
        cart.add_product(product)
        cart.remove_product(product, remove_count=1)
        assert not cart.products

    def test_cart_remove_more_than_added(self, cart, product):
        cart.add_product(product)
        cart.remove_product(product, remove_count=2)
        assert not cart.products

    def test_cart_def_buy_count(self, cart, product):
        cart.add_product(product)
        cart.remove_product(product)
        assert not cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, buy_count=3)
        cart.clear()
        assert not cart.products

    def test_get_total_price_one_item(self, cart, product):
        cart.add_product(product)
        assert cart.get_total_price() == product.price

    def test_get_total_price_some_products(self, cart, product, product_1):
        cart.add_product(product)
        cart.add_product(product_1)
        assert cart.get_total_price() == product.price + product_1.price

    def test_get_total_price_empty_cart(self, cart, product):
        assert cart.get_total_price() == 0.0

    def test_buy_some_items(self, cart, product, product_1):
        cart.add_product(product)
        cart.add_product(product_1, buy_count=50)
        cart.buy()
        assert product.check_quantity(999)
        assert product_1.check_quantity(0)
        assert not cart.products

    def test_cart_buy_more_than_avaiiable(self, cart, product_1):
        cart.add_product(product_1, buy_count=51)
        with pytest.raises(ValueError):
            cart.buy()

    def test_buy_empty_cart(self, cart):
        assert cart.get_total_price() == 0.0
        cart.buy()
        assert not cart.products
