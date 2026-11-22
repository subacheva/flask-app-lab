from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import select

from app.extensions import db
from app.models import Post, Tag, User
from app.posts import posts_bp
from app.posts.forms import PostForm, TagForm, UserForm


@posts_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data.strip(), content=form.content.data.strip(), posted=form.publish_date.data, category=form.category.data, is_active=form.enabled.data, author_id=form.author_id.data)
        post.tags = db.session.scalars(select(Tag).where(Tag.id.in_(form.tags.data))).all()
        db.session.add(post)
        db.session.commit()
        flash("Публікацію створено.", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/form.html", form=form, heading="Нова публікація")


@posts_bp.get("/post")
def all_posts():
    posts = db.session.scalars(select(Post).order_by(Post.posted.desc())).all()
    return render_template("posts/all.html", posts=posts)


@posts_bp.get("/post/<int:post_id>")
def detail_post(post_id):
    return render_template("posts/detail.html", post=db.get_or_404(Post, post_id))


@posts_bp.route("/post/<int:post_id>/update", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)
    if request.method == "GET":
        form.author_id.data = post.author_id
        form.tags.data = [tag.id for tag in post.tags]
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.posted = form.publish_date.data
        post.category = form.category.data
        post.author_id = form.author_id.data
        post.tags = db.session.scalars(select(Tag).where(Tag.id.in_(form.tags.data))).all()
        post.is_active = form.enabled.data
        db.session.commit()
        flash("Публікацію оновлено.", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))
    return render_template("posts/form.html", form=form, heading="Редагувати публікацію")


@posts_bp.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Публікацію видалено.", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/delete.html", post=post)


@posts_bp.route("/users/create", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        db.session.add(User(username=form.username.data.strip(), email=form.email.data.strip(), password=form.password.data))
        db.session.commit()
        flash("Користувача створено.", "success")
        return redirect(url_for("posts.all_users"))
    return render_template("posts/simple_form.html", form=form, heading="Новий автор")


@posts_bp.get("/users")
def all_users():
    users = db.session.scalars(select(User).order_by(User.id)).all()
    return render_template("posts/users.html", users=users)


@posts_bp.route("/tags/create", methods=["GET", "POST"])
def create_tag():
    form = TagForm()
    if form.validate_on_submit():
        db.session.add(Tag(name=form.name.data.strip()))
        db.session.commit()
        flash("Тег додано.", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/simple_form.html", form=form, heading="Новий тег")
