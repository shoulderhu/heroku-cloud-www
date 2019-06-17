import json
import requests as req
import sys
from time import sleep
from threading import Lock

host = "https://shoulderhu.tk:2096"
data = {"kind": "pyspark", "name": "cloud-www"}
headers = {"Content-Type": "application/json"}
ssid = ""
lock = Lock()


def create_spark():
    with lock:
        global ssid

        #if ssid != "":
            #state = get_sessions_state()
            #if state != "idle" and state != "busy":
                #delete_sessions()
                #ssid = ""
                #print("delete session " + state, file=sys.stdout)
            #else:
                #print("get session " + state, file=sys.stdout)
                #return

        tmpid = get_sessions()

        if tmpid != "":
            ssid = tmpid
            print("get session " + ssid, file=sys.stdout)
        else:
            ssid = post_sessions()
            print("post_session" + ssid, file=sys.stdout)
            while True:
                state = get_sessions_state()
                if state != "idle":
                    sleep(3)
                else:
                    break
            #post_statements(code_init(), False)
            post_statements(code_init2(), False)


def get_sessions():
    resp = req.get(f"{host}/sessions", headers=headers, verify=False).json()
    for session in resp["sessions"]:
        if session["name"] == data["name"]:
            return str(session["id"])
    return ""


def get_sessions_state():
    resp = req.get(f"{host}/sessions/{ssid}/state", headers=headers, verify=False).json()
    print(resp["state"])
    return resp["state"]


def post_sessions():
    resp = req.post(f"{host}/sessions",
                    data=json.dumps(data), headers=headers, verify=False).json()
    return str(resp["id"])


def post_statements(code, out=True):
    statements_url = f"{host}/sessions/{ssid}/statements"
    code_data = {"code": code}
    resp = req.post(statements_url, data=json.dumps(code_data),
                    headers=headers, verify=False).json()

    if out:
        statement_url = f"{statements_url}/{resp['id']}"
        return get_statements(statement_url)


def get_statements(statement_url):
    while True:
        resp = req.get(statement_url, headers=headers, verify=False).json()
        if resp["state"] != "available":
            sleep(1)
            continue
        else:
            resp_data = resp["output"]["data"]
            if "application/json" in resp_data:
                return resp_data["application/json"]
            elif "text/plain" in resp_data:
                return resp_data["text/plain"]


def delete_sessions():
    req.delete(f"{host}/sessions/{ssid}", headers=headers, verify=False)


def code_init():
    return """
text = sc.textFile("hdfs://name:9000/csv/student.csv")
first = text.first()
data = text.filter(lambda x: x != first)
data = data.map(lambda x: x.split(","))

def to_int(x):
    for i, j in enumerate(x[3:-2]):
        x[i + 3] = int(j)
    return x
def student_filter(school=None, div=None, level=None, grade=None, gender=None, loc=None, year=None):
    filter_data = data
    
    if school:
        filter_data = filter_data.filter(lambda x: x[0] == school)
    if div:
        filter_data = filter_data.filter(lambda x: x[1] == div)
    if level:
        filter_data = filter_data.filter(lambda x: x[2] == level)   
    if loc:
        filter_data = filter_data.filter(lambda x: x[19] == loc)
    if year:
        filter_data = filter_data.filter(lambda x: x[20] == year)
    if grade:
        if grade == "一年級":
            filter_data = filter_data.map(lambda x: x[0:5] + x[19:])
        elif grade == "二年級":
            filter_data = filter_data.map(lambda x: x[0:3] + x[5:7] + x[19:])
        elif grade == "三年級":
            filter_data = filter_data.map(lambda x: x[0:3] + x[7:9] + x[19:])
        elif grade == "四年級":
            filter_data = filter_data.map(lambda x: x[0:3] + x[9:11] + x[19:])
        elif grade == "五年級":
            filter_data = filter_data.map(lambda x: x[0:3] + x[11:13] + x[19:])
        elif grade == "六年級":
            filter_data = filter_data.map(lambda x: x[0:3] + x[13:15] + x[19:])
        elif grade == "七年級":
            filter_data = filter_data.map(lambda x: x[0:3] + x[15:17] + x[19:])
        elif grade == "延修生":
            filter_data = filter_data.map(lambda x: x[0:3] + x[17:])
        if gender == "男生":
            filter_data = filter_data.map(lambda x: x[0:4] + x[5:])
        elif gender == "女生":
            filter_data = filter_data.map(lambda x: x[0:3] + x[4:])
    if grade == None and gender:
        if gender == "男生":
            filter_data = filter_data.map(lambda x: x[0:3] + x[3:18:2] + x[19:])
        elif gender == "女生":
            filter_data = filter_data.map(lambda x: x[0:3] + x[4:19:2] + x[19:])
    
    filter_data = filter_data.map(to_int)
    return filter_data.map(lambda x: x[0:3] + [sum(x[3:-2])] + x[-2:]).collect()
"""


def code_init2():
    return """       
def aqi_filter():
    text = sc.textFile("hdfs://name:9000/csv/aqi.csv")
    first = text.first()
    data = text.filter(lambda x: x != first)
    data1 = data.map(lambda x: x.split(","))
    data2 = data1.filter(lambda x: x[6] == "左營")
    return data2.map(lambda x: x[3:4] + x[8:9]).collect()
"""