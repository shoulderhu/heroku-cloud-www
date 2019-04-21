from flask import current_app as app, url_for, json
import requests


def get(url):
    resp = requests.get(app.config["API_HOST"] + url_for(url))
    return json.loads(resp.text)


