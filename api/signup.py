from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from models.user import User
from models.engine.db_storage import DBStorage

app = Flask(__name__)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    password_verify = data.get('password_verify')
    birthday = data.get('birthday')
    
    # Optional fields
    boy_or_girl = data.get('boy_or_girl')

    # Validate required fields
    if not name or not email or not password or not password_verify or not birthday:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if password != password_verify:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(name=name, email=email, password=hashed_password, birthday=birthday, boy_or_girl=boy_or_girl)
    
    # Save to the database
    DBStorage.session.add(new_user)
    DBStorage.session.commit()

    return jsonify({'message': 'User created successfully! Please verify your email.'}), 201

from werkzeug.security import check_password_hash

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    # Fetch the user from the database
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        # Normally, you'd return a token here (JWT or session-based authentication)
        return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/user', methods=['GET'])
@jwt_required()  # Assuming JWT for authentication
def get_user_profile():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/user', methods=['PUT'])
@jwt_required()
def update_user_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update fields (add validation as needed)
    user.name = data.get('name', user.name)
    user.birthday = data.get('birthday', user.birthday)
    user.boy_or_girl = data.get('boy_or_girl', user.boy_or_girl)

    DBStorage.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/api/user', methods=['DELETE'])
@jwt_required()
def delete_user_account():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Delete the user
    DBStorage.session.delete(user)
    DBStorage.session.commit()

    return jsonify({'message': 'User account deleted successfully'}), 200
