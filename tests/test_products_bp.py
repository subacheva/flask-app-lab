import unittest

from app import app


class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list_shows_all_products_and_prices(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        for value in (b"Laptop", b"Phone", b"PC", b"1200", b"800", b"1800"):
            self.assertIn(value, response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Intel Core i7", response.data)
        self.assertIn(b"1200", response.data)

    def test_missing_product_returns_404(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)
