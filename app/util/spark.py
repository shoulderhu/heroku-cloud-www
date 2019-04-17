import json
import requests as req
import sys


def create_spark(host, data):
    ssid = get_sessions(host, data)
    if ssid != "":
        return ssid
    else:
        ssid = post_sessions(host, data)
        return ssid


def get_sessions(host, data):
    resp = req.get(host + "/sessions").json()
    for session in resp["sessions"]:
        if session["name"] == data["name"]:
            print("get session", file=sys.stdout)
            return str(session["id"])
    return ""


def post_sessions(host, data):
    resp = req.post(host + "/sessions",
                    data=json.dumps(data)).json()
    print("post_session", file=sys.stdout)
    return str(resp["id"])


def post_statements(code):
    pass


def get_statements():
    pass


def delete_sessions():
    pass
    #resp = req.get(host + "/sessions").json()

    #for session in resp["sessions"]:
    #    req.delete(host + "/sessions/" + str(session["id"]))
    #    print("delete_session: " + str(session["id"]), file=sys.stdout)
