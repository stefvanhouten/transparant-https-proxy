from api import db


class Configurations(db.Model):
    __tablename__ = "configurations"
    __table_args__ = (db.UniqueConstraint("ip", "name", name="uix_1"),)

    ip = db.Column(db.String(255), primary_key=True, nullable=False)
    name = db.Column(db.String(255), primary_key=True, nullable=False)
    block_iso = db.Column(db.Boolean)
    exclude_elements = db.Column(db.String(255))
