import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .routes import proxy

    app.register_blueprint(proxy.bp)
    return app
