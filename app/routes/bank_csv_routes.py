from flask import Blueprint, jsonify, request
from app import db
from app.models.bank_csv import BankCsv

bank_api = Blueprint('bank', __name__)


# Create a new bank
@bank_api.route('/create_bank', methods=['POST'])
def create_bank():
    data = request.get_json()
    new_bank = BankCsv(
        name=data['name'],
        date_column=data['date_column'],
        description_column=data.get('description_column'),
        credit_column=data['credit_column'],
        debit_column=data['debit_column']
    )
    db.session.add(new_bank)
    db.session.commit()
    return jsonify({
        'id': new_bank.id,
        'name': new_bank.name,
        'date_column': new_bank.date_column,
        'description_column': new_bank.description_column,
        'credit_column': new_bank.credit_column,
        'debit_column': new_bank.debit_column
    }), 201


# Get all banks
@bank_api.route('/', methods=['GET'])
def get_banks():
    banks = BankCsv.query.all()
    return jsonify([{
        'id': bank.id,
        'name': bank.name,
        'date_column': bank.date_column,
        'description_column': bank.description_column,
        'credit_column': bank.credit_column,
        'debit_column': bank.debit_column
    } for bank in banks])


# Get a specific bank by ID
@bank_api.route('/<int:bank_id>', methods=['GET'])
def get_bank(bank_id):
    bank = BankCsv.query.get_or_404(bank_id)
    return jsonify({
        'id': bank.id,
        'name': bank.name,
        'date_column': bank.date_column,
        'description_column': bank.description_column,
        'credit_column': bank.credit_column,
        'debit_column': bank.debit_column
    })


# Update a bank
@bank_api.route('/<int:bank_id>', methods=['PUT'])
def update_bank(bank_id):
    bank = BankCsv.query.get_or_404(bank_id)
    data = request.get_json()
    bank.name = data['name']
    bank.date_column = data['date_column']
    bank.description_column = data.get('description_column')
    bank.credit_column = data['credit_column']
    bank.debit_column = data['debit_column']
    db.session.commit()
    return jsonify({
        'id': bank.id,
        'name': bank.name,
        'date_column': bank.date_column,
        'description_column': bank.description_column,
        'credit_column': bank.credit_column,
        'debit_column': bank.debit_column
    })


# Delete a bank
@bank_api.route('/<int:bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    bank = BankCsv.query.get_or_404(bank_id)
    db.session.delete(bank)
    db.session.commit()
    return '', 204
