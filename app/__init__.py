import os

from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "local-development-key-change-before-deployment"
)

from app import views  # noqa: E402,F401
from app.products import products_bp  # noqa: E402
from app.users import users_bp  # noqa: E402

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp, url_prefix="/products")
