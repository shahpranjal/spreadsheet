from datetime import datetime
from dateutil import parser as date_parser
from sqlalchemy import Enum

from app import db
from app.models.base import Base


class Transaction(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    debit = db.Column(db.Float, nullable=False, default=0.0)
    credit = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank_csv.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', name='fk_transaction_category_id'), nullable=True)
    status = db.Column(Enum('pending', 'processed', 'skip', name='status_enum'), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, date, description, debit=0.0, credit=0.0, user_id=None, bank_id=None, category_id=None,
                 **kwargs):
        if not debit and not credit:
            raise ValueError("Either debit or credit must be provided.")

        self.set_date(date)
        self.description = description
        self.debit = debit
        self.credit = credit
        self.user_id = user_id
        self.bank_id = bank_id
        self.category_id = category_id
        super().__init__(**kwargs)

    def set_date(self, date):
        self.date = date_parser.parse(date) if isinstance(date, str) else date
