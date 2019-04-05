import os
import sys
from app import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app(os.environ.get("FLASK_CONFIG") or "default")

if __name__ == "__main__":
    app.run()
