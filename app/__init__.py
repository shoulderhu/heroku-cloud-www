import sys
from flask import Flask
from flask_sslify import SSLify
from config import config


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])

    sslify = SSLify(app, permanent=True)

    # print(app.config, file=sys.stdout)

    from .main import main
    app.register_blueprint(main)

    from .api import api
    app.register_blueprint(api, url_prefix="/api")

    return app

