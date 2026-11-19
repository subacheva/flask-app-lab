from flask import abort, flash, redirect, render_template, request, session, url_for
from sqlalchemy import select

from app.extensions import db
from app.posts import posts_bp
from app.posts.forms import DeletePostForm, PostForm
from app.posts.models import Post


@posts_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            posted=form.publish_date.data,
            category=form.category.data,
            is_active=form.enabled.data,
            author=session.get("username", "Anonymous")[:20],
        )
        db.session.add(post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.all_posts"))
    if form.is_submitted():
        flash("Please correct the errors in the form.", "error")
    return render_template("posts/add_post.html", title="Додати пост", form=form, heading="Додати пост")


@posts_bp.get("/post")
def all_posts():
    stmt = select(Post).where(Post.is_active.is_(True)).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts/posts.html", title="Публікації", posts=posts)


@posts_bp.get("/post/<int:post_id>")
def detail_post(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template("posts/detail_post.html", title=post.title, post=post)


@posts_bp.route("/post/<int:post_id>/update", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    if request.method == "GET":
        form = PostForm(data={
            "title": post.title,
            "content": post.content,
            "enabled": post.is_active,
            "publish_date": post.posted,
            "category": post.category,
        })
    else:
        form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data
        post.category = form.category.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))
    if form.is_submitted():
        flash("Please correct the errors in the form.", "error")
    return render_template("posts/add_post.html", title="Редагувати пост", form=form, heading="Редагувати пост")


@posts_bp.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = DeletePostForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/delete_confirm.html", title="Видалити пост", post=post, form=form)