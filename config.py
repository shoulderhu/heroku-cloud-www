import os


class Config:
    SECRET_KEY = os.urandom(16)
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class ProductionConfig(Config):
    pass


class HerokuConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "heroku": HerokuConfig,
    "default": DevelopmentConfig
}
