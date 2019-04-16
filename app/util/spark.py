import json
import requests as req
import sys

host = "https://shoulderhu.tk:2096" #app.config["LIVY_HOST"]
data = {"kind": "pyspark"}
headers = {"Content-Type": "application/json"}
session_path = ""
statement_path = ""


def create_spark():
    global session_path
    delete_sessions()
    resp = post_sessions()
    session_path = resp.headers["Location"]
    print(f"create_session: {session_path}", file=sys.stdout)


def post_sessions():
    global host, data, headers
    return req.post(host + "/sessions",
                    data=json.dumps(data),
                    headers=headers)


def post_statements(code):
    pass


def get_statements():
    pass


def delete_sessions():
    global host
    resp = req.get(host + "/sessions").json()

    for session in resp["sessions"]:
        req.delete(host + "/sessions/" + str(session["id"]))
        print("delete_session: " + str(session["id"]), file=sys.stdout)
