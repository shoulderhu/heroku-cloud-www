from . import api
from datetime import datetime, timedelta
from flask import current_app as app, request, jsonify
#from app.util.spark import post_statements, code_init2
from pyspark import SparkContext
from numpy import array
import numpy as np
from time import time


class AQI:
    def __init__(self, file=""):
        sc = SparkContext()
        self.csv = AQI.read_csv(sc, "file:/app/csv/aqi.csv")
        self.csv.persist()

    @staticmethod
    def read_csv(sc, name):
        text = sc.textFile(name)
        first = text.first()
        return text.filter(lambda x: x != first).map(lambda x: x.split(","))

    @staticmethod
    def get_idx(tab):
        if tab == "pm25-tab":
            return 0
        elif tab == "pm10-tab":
            return 1
        elif tab == "so2-tab":
            return 2
        elif tab == "o3-tab" or tab == "o3-8-tab":
            return 3
        elif tab == "no2-tab":
            return 4
        elif tab == "co-tab":
            return 5

    def filter_csv(self, tab, date, zone):
        t = time()
        idx = AQI.get_idx(tab)

        ret = dict()
        ret["data"] = []

        if tab == "o3-tab" or tab == "so2-tab" or tab == "no2-tab":
            filtered = self.filter_date_and_zone(date, zone)
            filtered.persist()

            ret["labels"], ret["label"] = AQI.gen_label(filtered)

            for loc in ret["label"]:
                ret["data"].append(AQI.map_loc(filtered, loc, idx))
                app.logger.info(f"[INFO] Location: {loc}")
        elif tab == "o3-8-tab" or tab == "co-tab":
            dmax, date2 = AQI.gen_date(date, 8)

            filtered = self.filter_date_and_zone(date2, zone, True)
            filtered.persist()

            ret["labels"], ret["label"] = AQI.gen_label(filtered)

            for loc in ret["label"]:
                ml = AQI.map_loc(filtered, loc, idx)
                start = ret["labels"].index(str(dmax))
                ret["labels"] = ret["labels"][start:]
                ret["data"].append(AQI.map_mean(ml, start, 8, 3 if tab == "o3-8-tab" else 1))
                app.logger.info(f"[INFO] Location: {loc}")
        elif tab == "pm25-tab" or tab == "pm10-tab":
            dmax, date2 = AQI.gen_date(date, 12)

            filtered = self.filter_date_and_zone(date2, zone, True)
            filtered.persist()

            ret["labels"], ret["label"] = AQI.gen_label(filtered)

            for loc in ret["label"]:
                ml = AQI.map_loc(filtered, loc, idx)
                start = ret["labels"].index(str(dmax))
                ret["labels"] = ret["labels"][start:]
                ret["data"].append(AQI.map_mean2(ml, start, 12, 4, 1 if tab == "pm25-tab" else None))
                app.logger.info(f"[INFO] Location: {loc}")

        app.logger.info(f"[INFO] Filter took {time() - t} s")
        return ret

    def filter_date_and_zone(self, date, zone, islist=False):
        if not islist:
            return self.csv.filter(lambda x: date in x[8] and zone == x[7])
        else:
            return self.csv.filter(lambda x: (zone == x[7]) and any(d in x[8] for d in date))

    @staticmethod
    def map_dates(filtered):
        return filtered.map(lambda x: x[8]).distinct().sortBy(lambda x: x).collect()

    @staticmethod
    def map_locs(filtered):
        return filtered.map(lambda x: x[6]).distinct().collect()

    @staticmethod
    def map_loc(filtered, loc, idx):
        return filtered.filter(lambda x: loc == x[6]).sortBy(lambda x: x[8]).map(lambda x: x[idx]).collect()

    @staticmethod
    def gen_date(date, h):
        dmax = datetime.strptime(date, "%Y-%m-%d")
        date2 = [date]

        for i in range(1, h + 1):
            date2.append(str(dmax - timedelta(hours=i)))

        return dmax, date2

    @staticmethod
    def gen_label(filtered):
        labels = AQI.map_dates(filtered)
        label = AQI.map_locs(filtered)
        app.logger.info(f"[INFO] Locations: {label}")
        return labels, label

    @staticmethod
    def map_mean(ml, start, h, ndigits):
        ml = list(map(float, ml))
        ret = []

        for i in range(start, len(ml)):
            r = ml[0:i] if i < h else ml[i - h:i]
            ret.append(0) if len(r) == 0 else ret.append(round(sum(r) / len(r), ndigits))

        return ret

    @staticmethod
    def map_mean2(ml, start, h1, h2, ndigits):
        ml = list(map(float, ml))
        ret = []

        for i in range(start, len(ml)):
            r1 = ml[0:i] if i < h1 else ml[i - h1:i]
            r2 = ml[0:i] if i < h2 else ml[i - h2:i]
            t1 = 0 if len(r1) == 0 else sum(r1) / len(r1)
            t2 = 0 if len(r2) == 0 else sum(r2) / len(r2)
            ret.append(round(t1 * 0.5 + t2 * 0.5, ndigits))

        return ret


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
    #data = post_statements(code)

    #data_table = {
    #    "draw": 0,
    #    "recordsTotal": len(data),
    #    "recordsFiltered": len(data),
    #    "data": data
    #}

    #resp = jsonify(data_table)
    #resp.headers.add("Access-Control-Allow-Origin", "*")
    #return resp


@api.route("/aqi", methods=["POST"])
def api():
    ret = aqi.filter_csv(request.form["tab"], request.form["date"], request.form["zone"])
    return jsonify(ret)



aqi = AQI()

