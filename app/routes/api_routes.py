from flask import Blueprint, request, jsonify
from app.models.transaction import Transaction
from app import db

api = Blueprint('api', __name__)


@api.route('/process-file', methods=['POST'])
def process_file():
    data = request.get_json()
    file_content = data.get('content')
    # process file content and store in the database
    # ...
    return jsonify({"message": "Data received and processed."}), 200
