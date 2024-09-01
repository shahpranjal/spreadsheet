from flask import Blueprint, request, jsonify
from app import db
from app.models import Transaction

transaction_api = Blueprint('transaction_api', __name__)


# Get all transactions
@transaction_api.route('/', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    transactions_data = [
        get_transaction_json(t) for t in transactions
    ]
    return jsonify(transactions_data), 200


# Create a new transaction
@transaction_api.route('/create', methods=['POST'])
def create_transaction():
    data = request.get_json()
    try:
        new_transaction = Transaction(
            date=data['date'],
            description=data['description'],
            debit=data.get('debit', 0.0),
            credit=data.get('credit', 0.0),
            user_id=data['user_id'],
            bank_id=data['bank_id'],
            category_id=data.get('category_id'),
        )
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({"message": "Transaction created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Update a transaction
@transaction_api.route('/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    data = request.get_json()

    try:
        # Update the transaction fields
        transaction.set_date(data.get('date', transaction.date))
        transaction.description = data.get('description', transaction.description)
        transaction.debit = data.get('debit', transaction.debit)
        transaction.credit = data.get('credit', transaction.credit)
        transaction.user_id = data.get('user_id', transaction.user_id)
        transaction.bank_id = data.get('bank_id', transaction.bank_id)
        transaction.category_id = data.get('category_id', transaction.category_id)
        transaction.status = data.get('status', transaction.status)

        if 'category_id' is None and transaction.status == 'processed':
            transaction.status = 'pending'

        db.session.commit()
        transaction = Transaction.query.get_or_404(transaction_id)
        return jsonify(
            {
                "message": "Transaction updated successfully!",
                "transaction": get_transaction_json(transaction)
            }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


def get_transaction_json(t):
    return {
        'id': t.id,
        'date': t.date.strftime('%Y-%m-%d'),
        'description': t.description,
        'debit': t.debit,
        'credit': t.credit,
        'user_id': t.user_id,
        'bank_id': t.bank_id,
        'category_id': t.category_id,
        'status': t.status,
        'created_at': t.created_at,
        'updated_at': t.updated_at
    }
