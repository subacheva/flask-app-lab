import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "local-development-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", "false").lower() == "true"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


configurations = {"development": DevelopmentConfig, "testing": TestingConfig, "production": ProductionConfig}
