from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)

ma = Marshmallow(app)
db = SQLAlchemy(app)


@app.cli.command("init-db")
def init_db():
    print("Initializing the database...")
    db.create_all()
    print("Database initialized successfully.")


@app.cli.command("remove-db")
def remove_db():
    print("Removing database...")
    db.drop_all()
    print("Database removed.")


from .routes import proxy

app.register_blueprint(proxy.bp)
