import sys
from flask import current_app as app, url_for, json
from . import main
from app.util.api import get


@main.route("/")
def index():
    text = get("api.index")
    #print(type(current_app.config["API_HOST"]), file=sys.stdout)
    return text["data"]

@main.route("/hello")
def index2():
    return "index"

@main.route("/hello4")
def index4():
    return "index4"