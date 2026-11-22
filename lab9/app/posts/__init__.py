from flask import Blueprint


posts_bp = Blueprint("posts", __name__, template_folder="templates")

from app.posts import views
