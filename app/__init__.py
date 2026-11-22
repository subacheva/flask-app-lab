import os
from pathlib import Path

from flask import Flask, render_template

from app.config import config_by_name
from app.extensions import db, migrate


def create_app(config_name=None):
    config_name = config_name or os.environ.get("APP_CONFIG", "development")
    config_class = config_by_name.get(config_name)
    if config_class is None:
        raise ValueError(f"Unknown application configuration: {config_name}")

    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(config_class)
    Path(application.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(application)
    migrate.init_app(application, db)

    from app import views
    from app.posts import posts_bp
    from app.products import products_bp
    from app.users import users_bp
    from app.posts import models as post_models
    from app.products import models as product_models

    views.register_main_routes(application)
    application.register_blueprint(users_bp, url_prefix="/users")
    application.register_blueprint(products_bp)
    application.register_blueprint(posts_bp)

    @application.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html", title="Сторінку не знайдено"), 404

    @application.errorhandler(413)
    def upload_too_large(error):
        return "Файл завеликий. Максимальний розмір — 2 МБ.", 413

    return application


app = create_app()
