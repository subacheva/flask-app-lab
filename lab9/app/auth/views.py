from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from app.auth import auth_bp
from app.auth.forms import LoginForm, RegistrationForm
from app.extensions import db
from app.models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.strip(), email=form.email.data.strip().lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Реєстрацію завершено. Ви увійшли в систему.", "success")
        return redirect(url_for("auth.account"))
    return render_template("auth/register.html", form=form, title="Реєстрація")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.email == form.email.data.strip().lower()))
        if user and user.check_password(form.password.data):
            login_user(user, remember=False)
            flash("Ви успішно увійшли.", "success")
            return redirect(url_for("auth.account"))
        flash("Неправильна електронна адреса або пароль.", "error")
    return render_template("auth/login.html", form=form, title="Вхід")


@auth_bp.get("/account")
@login_required
def account():
    return render_template("auth/account.html", title="Профіль")


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("auth.login"))
