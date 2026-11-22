from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import bcrypt, db, login_manager


post_tags = Table(
    "post_tags",
    db.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<User {self.username!r}>"


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    category: Mapped[str] = mapped_column(String(20), nullable=False, default="other")
    is_active: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped[User] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f"<Post {self.id}: {self.title!r}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    posts: Mapped[list[Post]] = relationship(secondary=post_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name!r}>"
