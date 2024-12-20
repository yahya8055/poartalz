from django.test import TestCase
from .models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product description.",
            price=99.99
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "A test product description.")
        self.assertEqual(float(self.product.price), 99.99)
