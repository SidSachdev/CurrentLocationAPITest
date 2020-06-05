import logging
import newrelic.agent


from flask import Flask, request, jsonify, Response
import uuid

from flask_sqlalchemy import SQLAlchemy
from voluptuous import Invalid

from analytics.tasks import (
    create_user_visit_helper,
    get_visit_by_id_helper,
    get_merchant_visit_helper,
)
from constants import ExceptionMessage
from exceptions import InputMalformed
from validator.request_validator import (
    validate_extract_create_user_visit_input,
    validate_extract_all_user_visit_input,
)
from database import metadata, get_db_session

app = Flask(__name__)
application = app

db = SQLAlchemy(metadata=metadata)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("app.py")


@app.route("/healthz")
def healthz():
    return "Health Check Complete"


@app.route("/ready")
def ready():
    return "Ready Check Complete"


@app.route("/api/v1/users/<user_id>/visits", methods=["POST"])
@newrelic.agent.function_trace()
def create_user_visit(user_id):
    """
    Function creates a new visit given the input post data
    :param user_id: Input param that represents the user_id
    :return: Success: Response with json output with the requested format
    """
    request_id = uuid.uuid4()
    try:
        data = validate_extract_create_user_visit_input(request)
        log.info("[{}] User visits requested for user: {}".format(request_id, user_id))
        return jsonify(
            create_user_visit_helper(
                get_db_session(), request_id, user_id, data.get("merchant")
            )
        )
    except Invalid as e:
        log.warning("[{}] Malformed input: {}".format(request_id, str(e)))
        return Response(ExceptionMessage.BAD_REQUEST, status=406)


@app.route("/api/v1/users/<user_id>/visits", methods=["GET"])
@newrelic.agent.function_trace()
def get_merchant_visit(user_id):
    """
    Function that given a search string, returns a list a merchant ids
    that match the given threshold
    :param user_id: Input param that represents the user_id
    :return: Success: Response with list of objects
    """
    request_id = uuid.uuid4()
    try:
        data = validate_extract_all_user_visit_input(request.args)
        log.info("[{}] User visits requested for user: {}".format(request_id, user_id))
        return jsonify(
            get_merchant_visit_helper(
                get_db_session(), request_id, user_id, data.get("searchString")
            )
        )
    except Invalid as e:
        log.warning(" Malformed input: {}".format(str(e)))
        return Response(InputMalformed(ExceptionMessage.BAD_REQUEST), status=406)


@app.route("/api/v1/visit/<visit_id>", methods=["GET"])
@newrelic.agent.function_trace()
def get_single_visit_by_id(visit_id):
    """
    Function gets a visit id by key
    :param visit_id: Input param that represents the user_id
    :return: Success: Response with json output with the requested format
    """
    request_id = uuid.uuid4()
    try:
        log.info(
            "[{}] User visits requested for visit ID: {}".format(request_id, visit_id)
        )
        return jsonify(get_visit_by_id_helper(get_db_session(), request_id, visit_id))
    except Invalid as e:
        log.warning("Malformed input: {}".format(str(e)))
        return Response(ExceptionMessage.BAD_REQUEST, status=406)
