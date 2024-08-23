from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


# class File(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     start_date = db.Column(db.Date, nullable=False)
#     end_date = db.Column(db.Date, nullable=False)
#     bank = db.Column(db.String(15), nullable=False)
#     person = db.Column(Person, nullable=False)
#     amount = db.Column(db.Float, nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bank = db.Column(db.String(15), nullable=False)
