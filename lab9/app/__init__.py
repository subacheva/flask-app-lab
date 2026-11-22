import os
from pathlib import Path

from flask import Flask, render_template

from app.config import configurations
from app.extensions import bcrypt, db, login_manager, migrate


def create_app(config_name=None):
    config_name = config_name or os.environ.get("APP_CONFIG", "development")
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(configurations[config_name])
    Path(application.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(application)
    migrate.init_app(application, db)
    bcrypt.init_app(application)
    login_manager.init_app(application)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Увійдіть, щоб відкрити цю сторінку."
    login_manager.login_message_category = "warning"

    from app import models
    from app.auth import auth_bp
    from app.posts import posts_bp

    application.register_blueprint(posts_bp)
    application.register_blueprint(auth_bp)

    @application.context_processor
    def inject_logout_form():
        from flask_wtf import FlaskForm
        return {"logout_form": FlaskForm()}

    @application.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return application
