from flask import Blueprint

web = Blueprint("web", __name__)


@web.route("/")
def home():
    return "API funcionando!"