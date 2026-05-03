from forex_python.converter import CurrencyRates
from stripe import StripeClient

from config.settings import STRIPE_API_KEY

api_key = STRIPE_API_KEY
client = StripeClient(api_key)


def convert_rub_to_usd(amount):
    """Конвертирует валют"""
    try:
        c = CurrencyRates()
        rate = c.get_rate("RUB", "USD")
        return int(amount * rate)
    except Exception as ex:
        return f"Что- то не так с конвертированием валют: {ex}"


def create_stripe_product(name):
    """Создаем stripe продукт"""

    product = client.v1.products.create({"name": name})
    return product


def create_stripe_price(product, price):
    """Создаем stripe цена продукта"""

    price = client.v1.prices.create(
        {
            "currency": "usd",
            "unit_amount": price * 100,
            "product_data": {"name": product["name"]},
        }
    )
    return price


def create_stipe_session(price):
    """Создаем сессию на оплату в страйпе"""

    session = client.v1.checkout.sessions.create(
        {
            "success_url": "http://127.0.0.1:8000/",
            "line_items": [{"price": price["id"], "quantity": 1}],
            "mode": "payment",
        }
    )
    return session["id"], session["url"]
