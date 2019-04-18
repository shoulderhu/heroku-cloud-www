import sys
from . import www
from flask import render_template
from app.util.api import get


@www.route("/")
def index():
    #text = get("api.index")
    #print(type(current_app.config["API_HOST"]), file=sys.stdout)
    #return text["data"]
    return render_template("index.html")


@www.route("/students")
def students():
    return render_template("students.html")
