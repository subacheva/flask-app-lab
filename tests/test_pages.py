import unittest

from app import app


class PagesTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage_uses_base_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Модульна структура Flask".encode(), response.data)
        self.assertIn(b"site-header", response.data)

    def test_resume_and_contacts_remain_available(self):
        self.assertEqual(self.client.get("/resume").status_code, 200)
        self.assertEqual(self.client.get("/contacts").status_code, 200)