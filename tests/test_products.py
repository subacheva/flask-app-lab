import io
import tempfile
import unittest
from pathlib import Path

from app import app


class ProductCRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            TINYDB_PATH=str(root / "data" / "products.json"),
            PRODUCT_UPLOAD_FOLDER=str(root / "uploads"),
        )
        self.client = app.test_client()
        self.product_data = {
            "name": "Keyboard",
            "content": "Механічна клавіатура для роботи.",
            "price": "1250.50",
            "category": "electronics",
            "quantity": "0",
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_create_product_and_prg_redirect(self):
        response = self.client.post("/product/add", data=self.product_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/product")
        listing = self.client.get("/product")
        self.assertIn(b"Keyboard", listing.data)
        self.assertIn(b"1250.50", listing.data)

    def test_uploaded_image_has_safe_name_and_is_displayed(self):
        data = dict(self.product_data)
        data["image"] = (io.BytesIO(b"image-data"), "my photo.JPG")
        response = self.client.post("/product/add", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 302)
        detail = self.client.get("/product/1")
        self.assertIn(b"/products/static/uploads/", detail.data)
        saved_files = list(Path(app.config["PRODUCT_UPLOAD_FOLDER"]).iterdir())
        self.assertEqual(len(saved_files), 1)
        self.assertNotEqual(saved_files[0].name, "my photo.JPG")

    def test_edit_preserves_id_and_created_at(self):
        self.client.post("/product/add", data=self.product_data)
        before = self.client.get("/product/1").data
        response = self.client.post("/product/1/edit", data={**self.product_data, "name": "New Keyboard"})
        self.assertEqual(response.status_code, 302)
        after = self.client.get("/product/1").data
        self.assertIn(b"New Keyboard", after)
        self.assertNotIn(b"<h1>Keyboard</h1>", after)
        self.assertIn("Кількість: 0".encode(), after)

    def test_delete_requires_confirmation_then_post_deletes(self):
        self.client.post("/product/add", data=self.product_data)
        response = self.client.get("/product/1/delete")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/product/1").status_code, 200)
        response = self.client.post("/product/1/delete")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get("/product/1").status_code, 404)

    def test_invalid_product_and_unknown_product(self):
        response = self.client.post("/product/add", data={**self.product_data, "name": "AB"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/product/987").status_code, 404)


if __name__ == "__main__":
    unittest.main()
