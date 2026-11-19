import os
from pathlib import Path

from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-development-key-change-before-deployment")
app.config["SESSION_COOKIE_SECURE"] = bool(os.environ.get("RENDER_EXTERNAL_URL"))
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
app.config["TINYDB_PATH"] = str(Path(__file__).resolve().parent.parent / "data" / "products.json")
app.config["PRODUCT_UPLOAD_FOLDER"] = str(Path(__file__).resolve().parent / "products" / "static" / "uploads")
app.config["CONTACT_LOG_PATH"] = str(Path(__file__).resolve().parent.parent / "logs" / "contacts.log")

from app import views  # noqa: E402,F401
from app.products import products_bp  # noqa: E402
from app.users import users_bp  # noqa: E402

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp)


@app.errorhandler(404)
def page_not_found(error):
    return "Сторінку не знайдено", 404


@app.errorhandler(413)
def upload_too_large(error):
    return "Файл завеликий. Максимальний розмір — 2 МБ.", 413