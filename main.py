import os
import sys

from app import create_app
from app.util.spark import create_spark
from dotenv import load_dotenv

# .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.environ.get("FLASK_CONFIG") or "default")

# spark
#if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN"):
#    app.config["LIVY_SSID"] = create_spark(app.config["LIVY_HOST"],
#                                           app.config["LIVY_DATA"])

if __name__ == "__main__":
    app.run()
