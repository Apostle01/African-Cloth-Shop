from decimal import Decimal

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from products.models import Product, Category
from cart.cart import Cart


class CartCalculationTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.category = Category.objects.create(
            name="Kente"
        )

        self.product1 = Product.objects.create(
            name="Red Kente",
            category=self.category,
            description="Original Bonwire Kente",
            price=Decimal("125.00"),
            stock=10
        )

        self.product2 = Product.objects.create(
            name="Blue Kente",
            category=self.category,
            description="Blue Kente fabric",
            price=Decimal("100.00"),
            stock=10
        )

    def create_request(self):
        request = self.factory.get("/")

        request.user = self.user

        middleware = SessionMiddleware(
            lambda request: None
        )

        middleware.process_request(request)
        request.session.save()

        return request

    def test_cart_total_with_multiple_products(self):
        request = self.create_request()

        cart = Cart(request)

        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=1)

        total = cart.get_total()

        expected_total = Decimal("350.00")

        self.assertEqual(
            Decimal(str(total)),
            expected_total
        )
