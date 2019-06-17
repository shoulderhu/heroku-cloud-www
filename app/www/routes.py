import os
import sys
from . import www
from flask import current_app as app, request, render_template, url_for, json, jsonify


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
                           title="大專院校校別學生數",
                           col=col,
                           url=app.config["API_HOST"])


@www.route("/aqi")
def aqi():
    with app.open_resource("static/json/www-aqi-tab.json") as f:
        tab = json.load(f)
    with app.open_resource("static/json/www-aqi-col.json") as f:
        col = json.load(f)
    return render_template("aqi.html", title="空氣品質指標(AQI)",
                           col=col, tab=tab)


@www.route("/test")
def test():
    pass

