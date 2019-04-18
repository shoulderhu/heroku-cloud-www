import os


class Config:
    SECRET_KEY = os.urandom(16)
    JSON_SORT_KEYS = False

    # Apache Livy
    LIVY_HOST = "https://shoulderhu.tk:2096"
    LIVY_DATA = {"kind": "pyspark", "name": "big-data-www"}
    LIVY_SSID = ""
    LIVY_STATEMENT = ""


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    API_HOST = "http://127.0.0.1:5000"


class ProductionConfig(Config):
    API_HOST = "https://big-data-www.herokuapp.com"


class HerokuConfig(ProductionConfig):
    pass


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "heroku": HerokuConfig,
    "default": DevelopmentConfig
}
