from flask import render_template, request

from app import app


@app.get("/")
def home():
    return render_template("homepage.html", title="Головна | Уляна Субачева")


@app.get("/resume")
def resume():
    return render_template("resume.html", title="Резюме | Уляна Субачева")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    return render_template(
        "contacts.html",
        title="Контакти | Уляна Субачева",
        sent=request.method == "POST",
    )