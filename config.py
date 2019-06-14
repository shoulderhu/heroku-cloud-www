import os


class Config:
    SECRET_KEY = os.urandom(16)
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    API_HOST = "http://127.0.0.1:5000"


class ProductionConfig(Config):
    API_HOST = os.environ.get("API_HOST")


class HerokuConfig(ProductionConfig):
    pass


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "heroku": HerokuConfig,
    "default": DevelopmentConfig
}
