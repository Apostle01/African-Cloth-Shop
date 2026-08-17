from django.test import TestCase

from decimal import Decimal
from django.contrib.auth.models import User
from products.models import Product, Category
from payment.models import Order, OrderItem


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.category = Category.objects.create(
            name="Kente"
        )

        self.product = Product.objects.create(
            name="Red Kente",
            category=self.category,
            description="Original Bonwire Kente",
            price=Decimal("125.00"),
            stock=10
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Test User",
            email="test@example.com",
            shipping_address="123 Test Street, London",
            total_price=Decimal("250.00")
        )

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.full_name, "Test User")
        self.assertEqual(order.email, "test@example.com")
        self.assertEqual(order.shipping_address, "123 Test Street, London")
        self.assertEqual(order.total_price, Decimal("250.00"))
        self.assertFalse(order.paid)
        self.assertEqual(order.status, "processing")


    def test_order_saved_and_retrieved(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Test Customer",
            email="customer@example.com",
            shipping_address="45 High Street, London",
            total_price=Decimal("250.00")
        )

        saved_order = Order.objects.get(id=order.id)

        self.assertEqual(saved_order.full_name, "Test Customer")
        self.assertEqual(saved_order.email, "customer@example.com")
        self.assertEqual(
            saved_order.shipping_address,
            "45 High Street, London"
        )
        self.assertEqual(
            saved_order.total_price,
            Decimal("250.00")
        )


    def test_order_has_primary_key(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Test Customer",
            email="customer@example.com",
            total_price=Decimal("125.00")
        )

        self.assertIsNotNone(order.pk)


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.category = Category.objects.create(
            name="Kente"
        )

        self.product = Product.objects.create(
            name="Red Kente",
            category=self.category,
            description="Original Bonwire Kente",
            price=Decimal("125.00"),
            stock=10
        )

        self.order = Order.objects.create(
            user=self.user,
            full_name="Test Customer",
            email="customer@example.com",
            total_price=Decimal("250.00")
        )


    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            user=self.user,
            price=Decimal("125.00"),
            quantity=2,
            price_paid=Decimal("250.00")
        )

        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.user, self.user)
        self.assertEqual(order_item.price, Decimal("125.00"))
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(
            order_item.price_paid,
            Decimal("250.00")
        )
        self.assertFalse(order_item.reviewed)


    def test_order_item_saved_and_retrieved(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            user=self.user,
            price=Decimal("125.00"),
            quantity=2,
            price_paid=Decimal("250.00")
        )

        saved_item = OrderItem.objects.get(id=order_item.id)

        self.assertEqual(saved_item.product, self.product)
        self.assertEqual(saved_item.quantity, 2)
        self.assertEqual(saved_item.price, Decimal("125.00"))
        self.assertEqual(
            saved_item.price_paid,
            Decimal("250.00")
        )


    def test_order_item_total_calculation(self):
        quantity = 2
        price = Decimal("125.00")

        item_total = price * quantity

        self.assertEqual(
            item_total,
            Decimal("250.00")
        )
