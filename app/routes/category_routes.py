from flask import Blueprint, jsonify, request
from app import db
from app.models.category import Category

category_api = Blueprint('categories', __name__)


# Create a new category
@category_api.route('/create_category', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'id': new_category.id, 'name': new_category.name}), 201


# Get all categories
@category_api.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': category.id, 'name': category.name} for category in categories])


# Get a specific category by ID
@category_api.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify({'id': category.id, 'name': category.name})


# Update a category
@category_api.route('/<int:category_id>', methods=['PUT'])
def update_user(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    category.name = data['name']
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name})


# Delete a category
@category_api.route('/<int:category_id>', methods=['DELETE'])
def delete_user(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return '', 204
