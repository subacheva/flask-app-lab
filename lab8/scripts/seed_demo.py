import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models import Post, Tag, User


app = create_app("development")

with app.app_context():
    if db.session.scalar(select(User.id).limit(1)):
        print("Demo data already exists.")
    else:
        authors = [
            User(username="olena", email="olena@example.com", password="demo"),
            User(username="andrii", email="andrii@example.com", password="demo"),
        ]
        tags = [Tag(name="Flask"), Tag(name="ORM"), Tag(name="Python")]
        db.session.add_all(authors + tags)
        db.session.flush()
        posts = [
            Post(
                title=f"Sample post {index}",
                content=f"Example post body number {index}.",
                author=authors[index % 2],
                tags=[tags[index % 3], tags[(index + 1) % 3]] if index == 1 else [tags[index % 3]],
            )
            for index in range(1, 6)
        ]
        db.session.add_all(posts)
        db.session.commit()
        print(f"Created {len(authors)} authors, {len(tags)} tags, and {len(posts)} posts.")
