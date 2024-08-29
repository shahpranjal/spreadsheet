from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User

user_api = Blueprint('user', __name__)


# Create a new user
@user_api.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name}), 201


# Get all users
@user_api.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])


# Get a specific user by ID
@user_api.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'name': user.name})


# Update a user
@user_api.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data['name']
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name})


# Delete a user
@user_api.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
