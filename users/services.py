import stripe
from django.conf import settings
from stripe import StripeClient


class PaymentByStripeService:
    """ Оплата курса с API Stripe """

    stripe.api_key = settings("STRIPE_API_KEY")


    def create_stripe_product(self, course):
        """ Создаем stripe продукт """
        name = course.title
        price = course.price
        client = StripeClient(
            "sk_test_51TSequQSPeVEH6I7Hg2Uw4MYZvehMVQPHuRADBeATuRHhNr4VNDZQvi2N2mZuROcmVSv0ieI9kcSPH47gRQsDRyl007Qft7vFn")

        product = client.v1.products.create({"name": name, "default_price": price})
        return product

    def create_stripe_price(self, product):
        """Создаем stripe цена продукта"""

        client = StripeClient(
            "sk_test_51TSequQSPeVEH6I7Hg2Uw4MYZvehMVQPHuRADBeATuRHhNr4VNDZQvi2N2mZuROcmVSv0ieI9kcSPH47gRQsDRyl007Qft7vFn")

        price = client.v1.prices.create({
            "currency": "usd",
            "unit_amount": product.get("default_price"),
            "product_data": product,
        })
        return price

    def create_stipe_session(self, price):
        """Создаем сессию на оплату в страйпе"""

        client = StripeClient(
            "sk_test_51TSey35QOA1pTSChPEKuAT3cxyKcUizSxaAio3ObgTtfI06OLPoq4UoDo4pYFenjkOyXicrXGNDwAmVxaVLYhYSy00BkJceV6M")

        session = client.v1.checkout.sessions.create({
            "success_url": "http://127.0.0.1:8000/",
            "line_items": [{"price": price.get("id"), "quantity": 1}],
            "mode": "payment",
        })
        return session.get("id"), session.get("url")







