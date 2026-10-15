from flask import redirect, render_template, request, url_for

from app.users import users_bp


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