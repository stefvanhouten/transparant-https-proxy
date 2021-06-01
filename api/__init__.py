from flask import Flask
from flask_marshmallow import Marshmallow

from .models import db

app = Flask(__name__)
ma = Marshmallow(app)
app.config.from_pyfile("config.py", silent=True)
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


from .routes import proxy

app.register_blueprint(proxy.bp)
