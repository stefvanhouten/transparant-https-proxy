from flask import Blueprint, jsonify

bp = Blueprint("proxy", __name__, url_prefix="/proxy")


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
