from functools import wraps
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from api.models import Configurations, db
from api.routes.schema import CreateConfigSchema, GetConfigSchema
from sqlalchemy.exc import IntegrityError

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
        except IntegrityError as err:
            db.session.rollback()
            return jsonify(
                {
                    "error": True,
                    "errors": ["Database error"],
                    "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                }
            )
        except Exception as err:
            print(err)
            return jsonify(
                {
                    "error": True,
                    "errors": ["Something went wrong"],
                    "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                }
            )

    return wrapper


@bp.route("/get_config/<ip>/<name>", methods=["GET"])
@error_wrapper
def get_config(ip, name):
    sanitzed_data = GetConfigSchema().load({"ip": ip, "name": name})

    config = Configurations.query.filter_by(
        ip=sanitzed_data["ip"], name=sanitzed_data["name"]
    ).first()

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

    return {
        "error": False,
        "errors": [],
        "config": CreateConfigSchema().dump(config),
        "status": HTTPStatus.OK,
    }


@bp.route("/create_config", methods=["POST"])
@error_wrapper
def create_config():
    sanitzed_data = CreateConfigSchema(session=db.session).load(request.get_json(), transient=True)

    if Configurations.query.filter_by(
        ip=sanitzed_data.ip, name=sanitzed_data.name
    ).first() is not None:
        return jsonify({
                "error": True,
                "errors": [
                    f"Config with the combination of '{sanitzed_data.ip}' and '{sanitzed_data.name}' already exists"
                ],
                "status": HTTPStatus.CONFLICT,
            })

    db.session.add(sanitzed_data)
    db.session.commit()

    return {
        "error": False,
        "errors": [],
        "config": CreateConfigSchema().dump(sanitzed_data),
        "status": HTTPStatus.OK,
    }

