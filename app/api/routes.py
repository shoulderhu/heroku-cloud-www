from flask import request, jsonify
from . import api
from app.util.spark import post_statements


@api.before_request
def before():
    pass


@api.route("/")
def index():
    return jsonify({"data": "Hello World"})


@api.route("/student", methods=["POST"])
def student():
    year = request.form["year"]
    school = request.form["school"]
    div = request.form["div"]
    level = request.form["level"]
    grade = request.form["grade"]
    gender = request.form["gender"]
    loc = request.form["loc"]
    parm = ""

    if year != "全":
        parm += f"year='{year}', "
    if school != "全":
        parm += f"school='{school}', "
    if div != "全":
        parm += f"div='{div}', "
    if level != "全":
        parm += f"level='{level}', "
    if grade != "全":
        parm += f"grade='{grade}', "
    if gender != "全":
        parm += f"gender='{gender}', "
    if loc != "全":
        parm += f"loc='{loc}', "

    code = f"""res = student_filter({parm[:-2]})\n%json res"""
    data = post_statements(code)

    data_table = {
        "draw": 0,
        "recordsTotal": len(data),
        "recordsFiltered": len(data),
        "data": data
    }

    return jsonify(data_table)


@api.route("/spark", methods=["GET", "POST"])
def spark():
    pass


