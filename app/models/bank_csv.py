from app import db
from app.models.base import Base


class BankCsv(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    date_column = db.Column(db.Integer, nullable=False)
    debit_column = db.Column(db.Integer, nullable=False)
    credit_column = db.Column(db.Integer, nullable=False)
    description_column = db.Column(db.Integer, nullable=False)
