import os
import sys
from . import www
from flask import current_app as app, render_template, url_for, json
from app.util.api import get


@www.route("/")
def index():
    with app.open_resource("static/json/www-index-cards.json") as f:
        cards = json.load(f)
    return render_template("index.html",
                           title="Big Data",
                           cards=cards["data"])


@www.route("/student")
def student():
    return render_template("student.html")

#text = get("api.index")
#print(type(current_app.config["API_HOST"]), file=sys.stdout)
#return text["data"]