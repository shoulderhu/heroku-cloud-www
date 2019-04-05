from . import main


@main.route("/")
def index():
    return "big-data-www"
