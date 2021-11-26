from flask import Flask, jsonify, make_response, request
from service import MailService
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/")
def hello_from_root():
    return jsonify(message="Hello from root!")


@app.route("/mail", methods=["POST"])
def mail():
    payload = request.get_json()
    USER_NAME = payload.get("user_name")
    TYPE = payload.get("type")
    TITLE = payload.get("title") or "勉強会"
    DATE = payload.get("date") or "1999/01/01 20:00 ~ 21:00"
    URL = payload.get("url") or "https://yahoo.co.jp"
    if USER_NAME is None:
        raise Exception("Invalid payload")
    MailService.send_email(USER_NAME, TYPE, TITLE, DATE, URL)

    return jsonify(message="Hello from path!")


@app.route("/debug", methods=["GET", "POST"])
def debug():
    payload = request.get_json()
    return jsonify(message=payload)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
