import unittest

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models import User


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def register(self, username="student", email="student@example.com", password="Password123"):
        return self.client.post("/register", data={"username": username, "email": email, "password": password, "confirm_password": password}, follow_redirects=True)

    def test_registration_page_loads_and_saves_hashed_password(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        response = self.register()
        self.assertEqual(response.status_code, 200)
        user = db.session.scalar(select(User).where(User.email == "student@example.com"))
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password, "Password123")
        self.assertTrue(user.check_password("Password123"))
        self.assertIn(b"student", response.data)

    def test_duplicate_username_and_email_are_rejected(self):
        self.register()
        self.client.post("/logout")
        response = self.register(username="student", email="another@example.com")
        self.assertIn("Це ім’я користувача вже зайняте.".encode(), response.data)
        response = self.register(username="another", email="student@example.com")
        self.assertIn("Ця електронна адреса вже зареєстрована.".encode(), response.data)

    def test_registration_rejects_invalid_email_and_mismatched_password(self):
        response = self.client.post("/register", data={"username": "newuser", "email": "invalid", "password": "Password123", "confirm_password": "other"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.scalar(select(User).where(User.username == "newuser")))

    def test_login_logout_and_protected_pages(self):
        response = self.client.get("/account", follow_redirects=True)
        self.assertIn("Вхід".encode(), response.data)
        self.register()
        self.client.post("/logout")
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/login", data={"email": "student@example.com", "password": "Password123"}, follow_redirects=True)
        self.assertIn("student".encode(), response.data)
        self.assertEqual(self.client.get("/users").status_code, 200)
        self.client.post("/logout")
        self.assertEqual(self.client.get("/users").status_code, 302)

    def test_login_rejects_wrong_password(self):
        self.register()
        self.client.post("/logout")
        response = self.client.post("/login", data={"email": "student@example.com", "password": "wrong"})
        self.assertIn("Неправильна".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
