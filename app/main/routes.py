import sys
from flask import render_template
from . import main
from app.util.api import get


@main.route("/")
def index():
    text = get("api.index")
    #print(type(current_app.config["API_HOST"]), file=sys.stdout)
    return text["data"]


@main.route("/test")
def test():
    return render_template("index.html")

@main.route("/hello4")
def index4():
    return "index4"