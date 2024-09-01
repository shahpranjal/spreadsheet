from app import db
from app.models.base import Base


class Category(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
