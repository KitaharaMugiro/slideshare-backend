from flask import Flask, jsonify, make_response, request
from service import MailService
from repository import ConferenceSubscriberRepository
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/")
def hello_from_root():
    return jsonify(message="Hello from root!")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    payload = request.get_json()
    authorization = request.headers.get("Authorization") or ""
    input = payload.get("input")
    conferenceId = input.get("conferenceId")
    resp = ConferenceSubscriberRepository.insertSubscribe(conferenceId, authorization)
    return jsonify(message=resp)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
