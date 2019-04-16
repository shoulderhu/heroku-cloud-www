import os
import sys

from app import create_app
from app.util.spark import create_spark
from dotenv import load_dotenv

# .env
if os.environ.get("WERKZEUG_RUN_MAIN"):
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

app = create_app(os.environ.get("FLASK_CONFIG") or "default")

# spark
# if os.environ.get("WERKZEUG_RUN_MAIN"):
create_spark()


if __name__ == "__main__":
    app.run()
