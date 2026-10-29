import unittest

from app import app


class AuthProfileTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def login(self):
        return self.client.post(
            "/users/login",
            data={"username": "student", "password": "flask123"},
            follow_redirects=True,
        )

    def test_profile_requires_login(self):
        response = self.client.get("/users/profile", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Увійдіть, щоб переглянути профіль.".encode(), response.data)

    def test_valid_login_and_logout(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Вітаємо, student!".encode(), response.data)
        self.assertIn("успішно увійшли".encode(), response.data)

        response = self.client.post("/users/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ви вийшли з системи.".encode(), response.data)
        self.assertEqual(self.client.get("/users/profile").status_code, 302)

    def test_invalid_login_shows_error(self):
        response = self.client.post(
            "/users/login",
            data={"username": "student", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Неправильне ім’я користувача або пароль.".encode(), response.data)

    def test_cookie_add_delete_and_delete_all(self):
        self.login()
        response = self.client.post(
            "/users/profile/cookies",
            data={"action": "add", "key": "favorite", "value": "green", "max_age": "3600"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("favorite".encode(), response.data)
        self.assertEqual(self.client.get_cookie("favorite").value, "green")

        response = self.client.post(
            "/users/profile/cookies",
            data={"action": "delete", "key": "favorite"},
            follow_redirects=True,
        )
        self.assertIsNone(self.client.get_cookie("favorite"))
        self.assertIn("Cookie «favorite» видалено.".encode(), response.data)

        self.client.set_cookie("one", "1")
        self.client.set_cookie("two", "2")
        self.client.post(
            "/users/profile/cookies", data={"action": "delete_all"}
        )
        self.assertIsNone(self.client.get_cookie("one"))
        self.assertIsNone(self.client.get_cookie("two"))

    def test_theme_is_saved_in_session(self):
        self.login()
        response = self.client.post("/users/profile/theme/dark", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<body class="theme-dark">', response.data)


if __name__ == "__main__":
    unittest.main()
