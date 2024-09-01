from flask import Blueprint, request, jsonify
from app.models import File, User, BankCsv

from app.services import FileProcessor

upload_api = Blueprint('upload', __name__)


@upload_api.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format, only CSV is supported"}), 400

    user_id = request.form['user_id']
    bank_id = request.form['bank_id']

    # Validate the input using the shared function
    validation_error, validated_data = validate_file_input(user_id, bank_id, file.filename)
    if validation_error:
        return jsonify(validation_error), 400

    file_processor = FileProcessor(file, validated_data['user'], validated_data['bank'])
    result = file_processor.process()

    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 201


def validate_file_input(user_id, bank_id, filename):
    # Validate user_id
    user = User.query.get(user_id)
    if not user:
        return {"error": "Invalid user_id, user does not exist"}, None

    # Validate bank_id
    bank = BankCsv.query.get(bank_id)
    if not bank:
        return {"error": "Invalid bank_id, bank does not exist"}, None

    # Check if the same file has already been uploaded
    existing_file = File.query.filter_by(
        user_id=user_id,
        bank_id=bank_id,
        filename=filename
    ).first()

    if existing_file:
        return {"error": "File with the same user, bank, date range, and filename has already been uploaded"}, None

    # If all validations pass
    return None, {"user": user, "bank": bank}
