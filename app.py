from flask import Flask, jsonify, make_response, request
from flask.globals import session
from service import MailService
from repository import ConferenceSubscriberRepository
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_from_root():
    return jsonify(message="Hello from root!")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    print("subscribe called")
    authorization = request.headers.get("Authorization")
    if not authorization:
        return make_response(jsonify(message="Missing authorization"), 401)

    payload = request.get_json()
    input = payload.get("input")
    conferenceId = input.get("conferenceId")
    username = input.get("username")
    conferenceTitle = input.get("conferenceTitle")
    date = input.get("date")
    url = input.get("url")

    # DB insert
    resp = ConferenceSubscriberRepository.insertSubscribe(conferenceId, authorization)

    # Send mail
    MailService.send_email_for_subscribing(username, conferenceTitle, date, url)
    return jsonify(message=resp)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
