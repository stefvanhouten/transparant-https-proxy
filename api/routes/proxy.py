from http import HTTPStatus
from functools import wraps
from marshmallow.exceptions import ValidationError

from flask import Blueprint, jsonify, request
from api.routes.schema import GetConfigSchema, CreateConfigSchema

bp = Blueprint("proxy", __name__, url_prefix="/proxy")

def error_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            return jsonify({
                "error": True,
                "errors": err.messages,
                "status": HTTPStatus.BAD_REQUEST
            })
        except Exception as err:
            print(err)
            return jsonify({
                "error": True,
                "errors": [],
                "status": HTTPStatus.INTERNAL_SERVER_ERROR
            })
    return wrapper

@bp.route("/")
def hello():
    return jsonify(
        {
            "exclude": [
                "script",
                "noscript",
                "html",
                "style",
            ]
        }
    )


@bp.route("/get_schema/<ip>", methods=["GET"])
@error_wrapper
def get_schema(ip):
    response = {}
    ip = GetConfigSchema().load({"ip": ip})
    return jsonify(
        {
            "exclude": [
                "script",
                "noscript",
                "html",
                "style",
            ]
        }
    )


@bp.route("/create_schema", methods=["POST"])
@error_wrapper
def create_schema():
    response = {}
    sanitzed_data = CreateConfigSchema().load(request.get_json())
    return jsonify(
        {
            "exclude": [
                "script",
                "noscript",
                "html",
                "style",
            ]
        }
    )


