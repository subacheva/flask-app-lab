import tempfile
import unittest
from pathlib import Path

from app import app


class ContactFormTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=False, CONTACT_LOG_PATH=str(Path(self.temp.name) / "contacts.log"))
        self.client = app.test_client()

    def tearDown(self):
        logger = __import__("logging").getLogger("contact_submissions")
        for handler in list(logger.handlers):
            handler.close()
            logger.removeHandler(handler)
        self.temp.cleanup()

    def test_contact_form_renders_and_valid_submission_redirects_and_logs(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/contact", data={"name": "Олена", "email": "olena@example.com", "topic": "project", "message": "Маю пропозицію для співпраці."})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/contact") or response.headers["Location"].endswith("/contacts"))
        log_text = Path(app.config["CONTACT_LOG_PATH"]).read_text(encoding="utf-8")
        self.assertIn("olena@example.com", log_text)
        self.assertIn("Маю пропозицію", log_text)

    def test_invalid_contact_data_shows_field_errors(self):
        response = self.client.post("/contacts", data={"name": "A", "email": "not-an-email", "topic": "project", "message": "short"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email address.", response.data)
        self.assertFalse(Path(app.config["CONTACT_LOG_PATH"]).exists())


if __name__ == "__main__":
    unittest.main()
