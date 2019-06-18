import os
from . import api
from datetime import datetime, timedelta
from flask import current_app as app, request, jsonify
#from app.util.spark import post_statements, code_init2
from pyspark import SparkContext
from time import time


class AQI:
    def __init__(self, file=""):
        sc = SparkContext()
        print(sc.master)
        self.csv = AQI.read_csv(sc, "hdfs://name:9000/csv/aqi.csv")
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
                ml = list(map(float, AQI.map_loc(filtered, loc, idx)))

                if tab == "o3-tab":
                    ml = list(map(lambda x: round(x / 1000, 3), ml))
                    ml = list(map(AQI.map_o3, ml))
                elif tab == "so2-tab":
                    ml = list(map(lambda x: round(x), ml))
                    ml = list(map(AQI.map_so2, ml))
                elif tab == "no2-tab":
                    ml = list(map(lambda x: round(x), ml))
                    ml = list(map(AQI.map_no2, ml))
                ret["data"].append(ml)
                app.logger.info(f"[INFO] Location: {loc}")
        elif tab == "o3-8-tab" or tab == "co-tab":
            dmax, date2 = AQI.gen_date(date, 8)

            filtered = self.filter_date_and_zone(date2, zone, True)
            filtered.persist()

            ret["labels"], ret["label"] = AQI.gen_label(filtered)
            start = ret["labels"].index(str(dmax))
            ret["labels"] = ret["labels"][start:]

            for loc in ret["label"]:
                ml = list(map(float, AQI.map_loc(filtered, loc, idx)))
                if tab == "o3-8-tab":
                    ml = list(map(lambda x: x / 1000, ml))
                ml = AQI.map_mean(ml, start, 8, 3 if tab == "o3-8-tab" else 1)

                if tab == "o3-8-tab":
                    ml = list(map(AQI.map_o3_8, ml))
                elif tab == "co-tab":
                    ml = list(map(AQI.map_co, ml))
                ret["data"].append(ml)
                app.logger.info(f"[INFO] Location: {loc}")
        elif tab == "pm25-tab" or tab == "pm10-tab":
            dmax, date2 = AQI.gen_date(date, 12)

            filtered = self.filter_date_and_zone(date2, zone, True)
            filtered.persist()

            ret["labels"], ret["label"] = AQI.gen_label(filtered)
            start = ret["labels"].index(str(dmax))
            ret["labels"] = ret["labels"][start:]

            for loc in ret["label"]:
                ml = list(map(float, AQI.map_loc(filtered, loc, idx)))
                ml = AQI.map_mean2(ml, start, 12, 4, 1 if tab == "pm25-tab" else None)

                if tab == "pm25-tab":
                    ml = list(map(AQI.map_pm25, ml))
                elif tab == "pm10-tab":
                    ml = list(map(AQI.map_pm10, ml))
                ret["data"].append(ml)
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
        ret = []

        for i in range(start, len(ml)):
            r = ml[0:i] if i < h else ml[i - h:i]
            ret.append(0) if len(r) == 0 else ret.append(round(sum(r) / len(r), ndigits))

        return ret

    @staticmethod
    def map_mean2(ml, start, h1, h2, ndigits):
        ret = []

        for i in range(start, len(ml)):
            r1 = ml[0:i] if i < h1 else ml[i - h1:i]
            r2 = ml[0:i] if i < h2 else ml[i - h2:i]
            t1 = 0 if len(r1) == 0 else sum(r1) / len(r1)
            t2 = 0 if len(r2) == 0 else sum(r2) / len(r2)
            ret.append(round(t1 * 0.5 + t2 * 0.5, ndigits))

        return ret

    @staticmethod
    def map_pm25(x):
        if 0 <= x <= 15.4:
            return round(x * 50 / 15.4)
        elif 15.5 <= x <= 35.4:
            return round((x - 15.5) * 49 / 19.9 + 51)
        elif 35.5 <= x <= 54.4:
            return round((x - 35.5) * 49 / 18.9 + 101)
        elif 54.5 <= x <= 150.4:
            return round((x - 54.5) * 49 / 95.9 + 151)
        elif 150.5 <= x <= 250.4:
            return round((x - 150.5) * 99 / 99.9 + 201)
        elif 250.5 <= x <= 350.4:
            return round((x - 250.5) * 99 / 99.9 + 301)
        elif 350.5 <= x <= 500.4:
            return round((x - 350.5) * 99 / 149.9 + 401)

    @staticmethod
    def map_pm10(x):
        if 0 <= x <= 54:
            return round(x * 50 / 54)
        elif 55 <= x <= 125:
            return round((x - 55) * 49 / 70 + 51)
        elif 126 <= x <= 254:
            return round((x - 126) * 49 / 128 + 101)
        elif 255 <= x <= 354:
            return round((x - 255) * 49 / 99 + 151)
        elif 355 <= x <= 424:
            return round((x - 355) * 99 / 69 + 201)
        elif 425 <= x <= 504:
            return round((x - 425) * 99 / 79 + 301)
        elif 505 <= x <= 604:
            return round((x - 505) * 99 / 99 + 401)

    @staticmethod
    def map_o3_8(x):
        if 0 <= x <= 0.054:
            return round(x * 50 / 0.054)
        elif 0.055 <= x <= 0.070:
            return round((x - 0.055) * 49 / 0.015 + 51)
        elif 0.071 <= x <= 0.085:
            return round((x - 0.071) * 49 / 0.014 + 101)
        elif 0.086 <= x <= 0.105:
            return round((x - 0.086) * 49 / 0.019 + 151)
        elif 0.106 <= x <= 0.2:
            return round((x - 0.106) * 99 / 0.094 + 201)
        else:
            return -1

    @staticmethod
    def map_co(x):
        if 0 <= x <= 4.4:
            return round(x * 50 / 4.4)
        elif 4.5 <= x <= 9.4:
            return round((x - 4.5) * 49 / 4.9 + 51)
        elif 9.5 <= x <= 12.4:
            return round((x - 9.5) * 49 / 2.9 + 101)
        elif 12.5 <= x <= 15.4:
            return round((x - 12.5) * 49 / 2.9 + 151)
        elif 15.5 <= x <= 30.4:
            return round((x - 15.5) * 99 / 14.9 + 201)
        elif 30.5 <= x <= 40.4:
            return round((x - 30.5) * 99 / 9.9 + 301)
        elif 40.5 <= x <= 50.4:
            return round((x - 40.5) * 99 / 9.9 + 401)

    @staticmethod
    def map_o3(x):
        if 0.125 <= x <= 0.164:
            return round((x - 0.125) * 49 / 0.039 + 101)
        elif 0.165 <= x <= 0.204:
            return round((x - 0.165) * 49 / 0.039 + 151)
        elif 0.205 <= x <= 0.404:
            return round((x - 0.205) * 99 / 0.199 + 201)
        elif 0.405 <= x <= 0.504:
            return round((x - 0.405) * 99 / 0.099 + 301)
        elif 0.505 <= x <= 0.604:
            return round((x - 0.505) * 99 / 0.099 + 401)
        else:
            return -1

    @staticmethod
    def map_so2(x):
        if 0 <= x <= 35:
            return round(x * 50 / 35)
        elif 36 <= x <= 75:
            return round((x - 36) * 49 / 39 + 51)
        elif 76 <= x <= 185:
            return round((x - 76) * 49 / 109 + 101)
        elif 186 <= x <= 304:
            return round((x - 186) * 49 / 118 + 151)
        elif 305 <= x <= 604:
            return round((x - 305) * 99 / 299 + 201)
        elif 605 <= x <= 804:
            return round((x - 605) * 99 / 199 + 301)
        elif 805 <= x <= 1004:
            return round((x - 805) * 99 / 199 + 401)

    @staticmethod
    def map_no2(x):
        if 0 <= x <= 53:
            return round(x * 50 / 53)
        elif 54 <= x <= 100:
            return round((x - 54) * 49 / 46 + 51)
        elif 101 <= x <= 360:
            return round((x - 101) * 49 / 259 + 101)
        elif 361 <= x <= 649:
            return round((x - 361) * 49 / 288 + 151)
        elif 650 <= x <= 1249:
            return round((x - 650) * 99 / 599 + 201)
        elif 1250 <= x <= 1649:
            return round((x - 1250) * 99 / 399 + 301)
        elif 1650 <= x <= 2049:
            return round((x - 1650) * 99 / 399 + 401)


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
    tab = request.form["tab"]
    date = request.form["date"]
    zone = request.form["zone"]

    if tab == "aqi-tab":
        MAX = None
        r, c = 0, 0

        for t in ["o3-8-tab", "o3-tab", "pm25-tab", "pm10-tab",
                  "co-tab", "so2-tab", "no2-tab"]:
            ret = aqi.filter_csv(t, date, zone)
            if MAX is None:
                MAX = ret["data"]
                r = len(MAX)
                c = len(MAX[0])
            else:
                data = ret["data"]
                for i in range(r):
                    for j in range(c):
                        MAX[i][j] = max(MAX[i][j], data[i][j])
        ret["data"] = MAX
    else:
        ret = aqi.filter_csv(tab, date, zone)

    resp = jsonify(ret)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


if os.environ.get("FLASK_BLUEPRINT") != "WWW":
    aqi = AQI()

