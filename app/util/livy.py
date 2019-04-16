import requests
import json

from flask import current_app as app

# host = app.config["LIVY_HOST"]
host = "https://shoulderhu.tk:2096"
data = {"kind": "pyspark"}
headers = {"Content-Type": "application/json"}


def spark_session():
    resp = requests.post(host + "/sessions",
                         data=json.dumps(data),
                         headers=headers)

spark_session()







