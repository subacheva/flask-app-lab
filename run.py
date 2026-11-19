import os

from app import create_app

app = create_app(os.environ.get("APP_CONFIG", "development"))


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))