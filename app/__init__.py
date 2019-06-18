import os
import sys

from config import config
from flask import Flask
from flask_sslify import SSLify


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])

    # SSL
    SSLify(app, permanent=True)

    app.logger.info(f"[INFO] FLASK_BLUEPRINT: {os.environ.get('FLASK_BLUEPRINT')}")

    if os.environ.get("FLASK_BLUEPRINT") != "API":
        from .www import www
        app.register_blueprint(www)

    if os.environ.get("FLASK_BLUEPRINT") != "WWW":
        from .api import api
        app.register_blueprint(api, url_prefix="/api")

    return app

