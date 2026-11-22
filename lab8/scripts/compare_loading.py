import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import event, select
from sqlalchemy.orm import joinedload, selectinload

from app import create_app
from app.extensions import db
from app.models import Post


app = create_app("development")


def measure(optimized):
    statements = []

    def count_select(connection, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    with app.app_context():
        event.listen(db.engine, "before_cursor_execute", count_select)
        try:
            db.session.remove()
            query = select(Post).order_by(Post.id)
            if optimized:
                query = query.options(joinedload(Post.author), selectinload(Post.tags))
            posts = db.session.scalars(query).unique().all()
            for post in posts:
                print(post.title, post.author.username, [tag.name for tag in post.tags])
            print("Posts:", len(posts), "SELECT:", len(statements))
        finally:
            event.remove(db.engine, "before_cursor_execute", count_select)
            db.session.remove()


if __name__ == "__main__":
    print("Without eager loading")
    measure(False)
    print("With joinedload(author) and selectinload(tags)")
    measure(True)
