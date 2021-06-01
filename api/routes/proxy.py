from functools import wraps
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from api.models import Configurations
from api.routes.schema import CreateConfigSchema, GetConfigSchema

bp = Blueprint("proxy", __name__, url_prefix="/proxy")


def error_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            return jsonify(
                {
                    "error": True,
                    "errors": err.messages,
                    "status": HTTPStatus.BAD_REQUEST,
                }
            )
        except Exception as err:
            print(err)
            return jsonify(
                {
                    "error": True,
                    "errors": [],
                    "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                }
            )

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


@bp.route("/get_schema/<ip>/<name>", methods=["GET"])
@error_wrapper
def get_schema(ip, name):
    response = {
        "error": False,
        "errors": [],
        "config": None,
        "status": HTTPStatus.OK,
    }
    sanitzed_data = GetConfigSchema().load({"ip": ip, "name": name})

    config = Configurations.query.filter_by(
        ip=sanitzed_data["ip"], name=sanitzed_data["name"]
    ).first()

    data = CreateConfigSchema(exclude=["exclude_elements"]).dump(config)
    exclude_elements = []

    if not config:
        return jsonify(
            {
                "error": True,
                "errors": [
                    f"Config with combination ip: '{ip}' and name: '{name}' not found"
                ],
                "status": HTTPStatus.NOT_FOUND,
            }
        )

    # Quick and dirty fix
    if len(config.exclude_elements) != 0:
        items = config.exclude_elements.split(",")
        for element in items:
            exclude_elements.append(element)
        data["exclude_elements"] = exclude_elements

    response["config"] = data
    return response


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
