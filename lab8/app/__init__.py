import os
from pathlib import Path

from flask import Flask, render_template

from app.config import configurations
from app.extensions import db, migrate


def create_app(config_name=None):
    config_name = config_name or os.environ.get("APP_CONFIG", "development")
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(configurations[config_name])
    Path(application.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(application)
    migrate.init_app(application, db)

    from app.posts import posts_bp
    from app import models

    application.register_blueprint(posts_bp)

    @application.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return application
