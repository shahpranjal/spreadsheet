from flask import Blueprint, render_template
from app.models.bank_csv import BankCsv

process_file = Blueprint('process_file', __name__)


@process_file.route('/')
def index():
    banks = BankCsv.query.all()
    return render_template('upload_file.html', banks=banks)
