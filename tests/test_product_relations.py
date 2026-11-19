import unittest

from app import create_app, db
from app.products.models import Category, Product


class ProductRelationshipTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")

    def setUp(self):
        self.context = self.app.app_context()
        self.context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def test_product_category_relationship_and_defaults(self):
        category = Category(name="Laptops")
        product = Product(name="Gaming Laptop", price=1500, active=False, category=category)
        db.session.add(product)
        db.session.commit()

        loaded_product = db.session.get(Product, product.id)
        loaded_category = db.session.get(Category, category.id)
        self.assertEqual(loaded_product.category.name, "Laptops")
        self.assertEqual(loaded_category.products[0].name, "Gaming Laptop")
        self.assertFalse(loaded_product.active)
        self.assertIsNotNone(loaded_product.created_at)

    def test_active_defaults_to_true(self):
        product = Product(name="iPhone 15", price=999.99)
        db.session.add(product)
        db.session.commit()
        self.assertTrue(db.session.get(Product, product.id).active)


if __name__ == "__main__":
    unittest.main()
