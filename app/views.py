from flask import flash, redirect, render_template, url_for

from app.forms import ContactForm


def home():
    return render_template("homepage.html", title="Головна | Уляна Субачева")


def resume():
    return render_template("resume.html", title="Резюме | Уляна Субачева")


def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        from pathlib import Path
        import logging
        from flask import current_app

        log_path = Path(current_app.config["CONTACT_LOG_PATH"])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger("contact_submissions")
        if not logger.handlers:
            handler = logging.FileHandler(log_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.propagate = False
        logger.info("contact name=%r email=%r topic=%r message=%r", form.name.data, form.email.data, form.topic.data, form.message.data)
        flash("Дякую! Повідомлення успішно збережено.", "success")
        return redirect(url_for("contacts"))
    if form.is_submitted():
        flash("Перевірте поля форми та виправте помилки.", "error")
    return render_template("contacts.html", title="Контакти | Уляна Субачева", form=form)


def register_main_routes(application):
    application.add_url_rule("/", endpoint="home", view_func=home, methods=["GET"])
    application.add_url_rule("/resume", endpoint="resume", view_func=resume, methods=["GET"])
    application.add_url_rule("/contacts", endpoint="contacts", view_func=contacts, methods=["GET", "POST"])
    application.add_url_rule("/contact", endpoint="contacts_legacy", view_func=contacts, methods=["GET", "POST"])
