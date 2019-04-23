import os
import sys
from . import www
from flask import current_app as app, request, render_template, url_for, json, jsonify
from app.util.api import get


@www.route("/")
def index():
    with app.open_resource("static/json/www-index-card.json") as f:
        cards = json.load(f)
    return render_template("index.html",
                           title="Big Data",
                           cards=cards["data"])


@www.route("/student")
def student():
    with app.open_resource("static/json/www-student-col.json") as f:
        col = json.load(f)
    return render_template("student.html",
                           col=col,
                           url=app.config["API_HOST"])


@www.route("/test")
def test():
    pass
    #with app.open_resource("static/json/www-student-col.json") as f:
    #    col = json.load(f)
    #return render_template("test.html", col=col)
#text = get("api.index")
#print(type(current_app.config["API_HOST"]), file=sys.stdout)
#return text["data"]
