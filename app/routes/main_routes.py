from flask import Blueprint, render_template
from app.models.bank_csv import BankCsv

main = Blueprint('main', __name__)


@main.route('/')
def index():
    banks = BankCsv.query.all()
    return render_template('index.html', banks=banks)
