from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)

ma = Marshmallow(app)
db = SQLAlchemy(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()

@app.cli.command("remove-db")
def remove_db():
    db.drop_all()

from .routes import proxy

app.register_blueprint(proxy.bp)
