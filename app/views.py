import logging
from pathlib import Path

from flask import current_app, flash, redirect, render_template, url_for

from app import app
from app.forms import ContactForm


@app.get("/")
def home():
    return render_template("homepage.html", title="Головна | Уляна Субачева")


@app.get("/resume")
def resume():
    return render_template("resume.html", title="Резюме | Уляна Субачева")


@app.route("/contacts", methods=["GET", "POST"])
@app.route("/contact", methods=["GET", "POST"])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        log_path = Path(current_app.config["CONTACT_LOG_PATH"])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger("contact_submissions")
        if not logger.handlers:
            handler = logging.FileHandler(log_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.propagate = False
        logger.info(
            "contact name=%r email=%r topic=%r message=%r",
            form.name.data,
            form.email.data,
            form.topic.data,
            form.message.data,
        )
        flash("Дякую! Повідомлення успішно збережено.", "success")
        return redirect(url_for("contacts"))
    return render_template("contacts.html", title="Контакти | Уляна Субачева", form=form)