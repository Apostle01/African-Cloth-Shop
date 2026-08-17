from decimal import Decimal

from django.test import TestCase

from products.models import Product, Category


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Kente"
        )

    def test_product_creation(self):
        product = Product.objects.create(
            name="Red Kente",
            category=self.category,
            description="Original Bonwire Kente",
            price=Decimal("125.00"),
            stock=10
        )

        self.assertEqual(product.name, "Red Kente")
        self.assertEqual(
            product.description,
            "Original Bonwire Kente"
        )
        self.assertEqual(
            product.price,
            Decimal("125.00")
        )
        self.assertEqual(product.stock, 10)

    def test_product_saved_and_retrieved(self):
        product = Product.objects.create(
            name="Yellow and Blue",
            category=self.category,
            description="Plain yellow and blue Kente",
            price=Decimal("100.00"),
            stock=10
        )

        saved_product = Product.objects.get(id=product.id)

        self.assertEqual(
            saved_product.name,
            "Yellow and Blue"
        )
        self.assertEqual(
            saved_product.description,
            "Plain yellow and blue Kente"
        )
        self.assertEqual(
            saved_product.price,
            Decimal("100.00")
        )
        self.assertEqual(
            saved_product.stock,
            10
        )

    def test_all_product_fields_are_stored_correctly(self):
        product = Product.objects.create(
            name="White Gold",
            category=self.category,
            description="White and Gold coloured Kente",
            price=Decimal("100.00"),
            stock=10
        )

        product_from_db = Product.objects.get(pk=product.pk)

        self.assertEqual(
            product_from_db.name,
            "White Gold"
        )
        self.assertEqual(
            product_from_db.description,
            "White and Gold coloured Kente"
        )
        self.assertEqual(
            product_from_db.price,
            Decimal("100.00")
        )
        self.assertEqual(
            product_from_db.stock,
            10
        )

    def test_product_has_primary_key(self):
        product = Product.objects.create(
            name="Strawberry Kente",
            category=self.category,
            price=Decimal("125.00"),
            stock=10
        )

        self.assertIsNotNone(product.pk)

    def test_product_count(self):
        Product.objects.create(
            name="Green Kente",
            category=self.category,
            price=Decimal("125.00"),
            stock=10
        )

        Product.objects.create(
            name="Red Kente",
            category=self.category,
            price=Decimal("125.00"),
            stock=10
        )

        self.assertEqual(Product.objects.count(), 2)

    def test_current_price_when_product_is_on_sale(self):
        product = Product.objects.create(
            name="Sale Kente",
            category=self.category,
            price=Decimal("150.00"),
            sale_price=Decimal("125.00"),
            is_sale=True,
            stock=10
        )

        self.assertEqual(
            product.current_price,
            Decimal("125.00")
        )

    def test_current_price_when_product_is_not_on_sale(self):
        product = Product.objects.create(
            name="Regular Kente",
            category=self.category,
            price=Decimal("150.00"),
            sale_price=Decimal("125.00"),
            is_sale=False,
            stock=10
        )

        self.assertEqual(
            product.current_price,
            Decimal("150.00")
        )

    def test_product_in_stock(self):
        product = Product.objects.create(
            name="Available Kente",
            category=self.category,
            price=Decimal("125.00"),
            stock=10
        )

        self.assertTrue(product.in_stock())