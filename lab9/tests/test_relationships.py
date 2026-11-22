import unittest

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models import Post, Tag, User


class RelationshipTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.author = User(username="author", email="author@example.com")
        self.tag = Tag(name="orm")
        self.second_tag = Tag(name="python")
        db.session.add_all([self.author, self.tag, self.second_tag])
        db.session.commit()
        self.post = Post(title="Post", content="Body", author=self.author, tags=[self.tag])
        db.session.add(self.post)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def test_bidirectional_user_post_relationship(self):
        self.assertEqual(self.author.posts[0].title, "Post")
        self.assertEqual(self.post.author.username, "author")

    def test_many_to_many_relationship(self):
        self.assertEqual(self.post.tags[0].name, "orm")
        self.assertEqual(self.tag.posts[0].title, "Post")

    def test_post_detail_displays_author_and_tags(self):
        response = self.client.get(f"/post/{self.post.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"author", response.data)
        self.assertIn(b"orm", response.data)

    def test_form_loads_authors_and_multiple_tags_and_saves_them(self):
        form_page = self.client.get("/post/create")
        self.assertIn("author".encode(), form_page.data)
        self.assertIn("python".encode(), form_page.data)
        response = self.client.post("/post/create", data={
            "title": "New post",
            "content": "Post with selected author and tags.",
            "publish_date": "2026-11-22T10:00",
            "category": "tech",
            "author_id": str(self.author.id),
            "tags": [str(self.tag.id), str(self.second_tag.id)],
            "enabled": "y",
        })
        self.assertEqual(response.status_code, 302)
        post = db.session.scalar(select(Post).where(Post.title == "New post"))
        self.assertEqual(post.author.username, "author")
        self.assertEqual({tag.name for tag in post.tags}, {"orm", "python"})


if __name__ == "__main__":
    unittest.main()
