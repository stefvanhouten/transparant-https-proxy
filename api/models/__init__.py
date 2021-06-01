from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import UniqueConstraint

db = SQLAlchemy()


class Configurations(db.Model):
    __tablename__ = "configurations"
    ip = db.Column(db.String(255), primary_key=True, nullable=False)
    name = db.Column(db.String(255), primary_key=True, nullable=False)
    block_iso = db.Column(db.Boolean)
    exclude_elements = db.Column(db.String(255))

    UniqueConstraint("ip", "name", name="uix_1")
