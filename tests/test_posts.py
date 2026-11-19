import unittest

from app import create_app, db
from app.posts.models import Post


class PostsCRUDTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")

    def setUp(self):
        self.context = self.app.app_context()
        self.context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def create_post(self, title="First post"):
        return self.client.post("/post/create", data={
            "title": title,
            "content": "This is the full body of the post.",
            "enabled": "y",
            "publish_date": "2026-11-19T12:30",
            "category": "publication",
        })

    def test_create_post_uses_prg_and_default_author(self):
        response = self.create_post()
        self.assertEqual(response.status_code, 302)
        post = db.session.scalar(db.select(Post))
        self.assertIsNotNone(post)
        self.assertEqual(post.author, "Anonymous")
        self.assertTrue(post.is_active)
        self.assertEqual(post.category, "publication")

    def test_list_shows_active_posts_only_and_details_show_post(self):
        self.create_post()
        inactive = Post(title="Hidden", content="Not public", is_active=False, author="student")
        db.session.add(inactive)
        db.session.commit()
        listing = self.client.get("/post")
        self.assertIn(b"First post", listing.data)
        self.assertNotIn(b"Hidden", listing.data)
        detail = self.client.get("/post/1")
        self.assertEqual(detail.status_code, 200)
        self.assertIn(b"Anonymous", detail.data)

    def test_edit_prefills_and_updates_post(self):
        self.create_post()
        form = self.client.get("/post/1/update")
        self.assertIn(b"First post", form.data)
        response = self.client.post("/post/1/update", data={
            "title": "Updated post",
            "content": "Updated body content.",
            "enabled": "y",
            "publish_date": "2026-11-20T09:45",
            "category": "tech",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(db.session.get(Post, 1).title, "Updated post")
        self.assertEqual(db.session.get(Post, 1).category, "tech")

    def test_delete_requires_post_confirmation(self):
        self.create_post()
        confirmation = self.client.get("/post/1/delete")
        self.assertEqual(confirmation.status_code, 200)
        self.assertIsNotNone(db.session.get(Post, 1))
        response = self.client.post("/post/1/delete")
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(db.session.get(Post, 1))

    def test_not_found_pages_use_custom_template(self):
        response = self.client.get("/post/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Сторінку не знайдено".encode(), response.data)


if __name__ == "__main__":
    unittest.main()