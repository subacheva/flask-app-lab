import re

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.users import users_bp


# Demo credentials for this lab; replace with a real user store in production.
DEMO_USERNAME = "student"
DEMO_PASSWORD = "flask123"
COOKIE_KEY_PATTERN = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
MAX_COOKIE_AGE = 60 * 60 * 24 * 365


@users_bp.get("/hi/<name>")
def greetings(name):
    age = request.args.get("age", "")
    return render_template(
        "users/hi.html",
        title=f"Вітаємо, {name} | Користувачі",
        name=name.upper(),
        age=age,
    )


@users_bp.get("/admin")
def admin():
    return redirect(url_for("users.greetings", name="Administrator", age=45))


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session.clear()
            session["username"] = username
            flash("Ви успішно увійшли в систему.", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильне ім’я користувача або пароль.", "error")

    return render_template("users/login.html", title="Вхід")


@users_bp.get("/profile")
def profile():
    username = session.get("username")
    if not username:
        flash("Увійдіть, щоб переглянути профіль.", "error")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("profile_theme", "light")
    if theme not in {"light", "dark"}:
        theme = "light"
    cookies = [
        {"key": key, "value": value}
        for key, value in sorted(request.cookies.items())
        if key != current_app.config["SESSION_COOKIE_NAME"]
    ]
    return render_template(
        "users/profile.html",
        title="Профіль",
        username=username,
        theme=theme,
        cookies=cookies,
    )


@users_bp.post("/logout")
def logout():
    session.clear()
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.post("/profile/cookies")
def manage_cookies():
    if not session.get("username"):
        flash("Увійдіть, щоб керувати cookie.", "error")
        return redirect(url_for("users.login"))

    action = request.form.get("action")
    response = redirect(url_for("users.profile"))
    session_cookie = current_app.config["SESSION_COOKIE_NAME"]

    if action == "add":
        key = request.form.get("key", "").strip()
        value = request.form.get("value", "")
        max_age_value = request.form.get("max_age", "").strip()
        if not COOKIE_KEY_PATTERN.fullmatch(key) or key == session_cookie:
            flash("Вкажіть коректний ключ cookie.", "error")
            return response
        if not value:
            flash("Значення cookie не може бути порожнім.", "error")
            return response
        if max_age_value:
            try:
                max_age = int(max_age_value)
            except ValueError:
                max_age = 0
            if not 1 <= max_age <= MAX_COOKIE_AGE:
                flash("Термін дії має бути від 1 до 31 536 000 секунд.", "error")
                return response
        else:
            max_age = None
        response.set_cookie(key, value, max_age=max_age, httponly=True, samesite="Lax")
        flash(f"Cookie «{key}» додано.", "success")
    elif action == "delete":
        key = request.form.get("key", "").strip()
        if not key or key == session_cookie:
            flash("Вкажіть ключ cookie, яку потрібно видалити.", "error")
            return response
        if key not in request.cookies:
            flash(f"Cookie «{key}» не знайдено.", "warning")
            return response
        response.delete_cookie(key)
        flash(f"Cookie «{key}» видалено.", "success")
    elif action == "delete_all":
        cookie_names = [
            key for key in request.cookies if key != session_cookie
        ]
        for key in cookie_names:
            response.delete_cookie(key)
        if cookie_names:
            flash("Усі cookie сайту видалено.", "success")
        else:
            flash("Немає cookie для видалення.", "warning")
    else:
        abort(400)

    return response


@users_bp.post("/profile/theme/<theme>")
def set_theme(theme):
    if not session.get("username"):
        flash("Увійдіть, щоб змінити кольорову схему.", "error")
        return redirect(url_for("users.login"))
    if theme not in {"light", "dark"}:
        abort(404)
    response = redirect(url_for("users.profile"))
    response.set_cookie(
        "profile_theme",
        theme,
        max_age=MAX_COOKIE_AGE,
        httponly=True,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite="Lax",
    )
    flash("Кольорову схему оновлено.", "success")
    return response
