from app import db
from datetime import datetime

from app.models.base import Base


class File(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False, default='csv')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank_csv.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
