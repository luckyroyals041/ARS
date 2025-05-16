from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import timedelta
import traceback

from . import auth_bp
from .models import get_user_by_username, create_user, verify_password
from .decorators import role_required

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user and return JWT tokens."""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Username and password are required"}), 400
        
        username = data['username']
        password = data['password']
        
        # Get user from database
        user = get_user_by_username(username)
        
        # Check if user exists and password is correct
        if not user or not verify_password(user, password):
            return jsonify({"error": "Invalid username or password"}), 401
        
        # Check if user is active
        if not user['is_active']:
            return jsonify({"error": "Account is inactive"}), 403
        
        # Create identity object with minimal user info
        identity = {
            "id": user['id'],
            "username": user['username'],
            "role": user['role'],
            "department": user['department']
        }
        
        # Create access and refresh tokens
        access_token = create_access_token(
            identity=identity,
            expires_delta=timedelta(hours=1)
        )
        
        refresh_token = create_refresh_token(
            identity=identity,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "role": user['role'],
                "department": user['department'],
                "email": user['email']
            },
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        })
        
    except Exception as e:
        print(f"Error in login: {e}")
        traceback.print_exc()
        return jsonify({"error": "Login failed"}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user (for development purposes only)."""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check if username already exists
        existing_user = get_user_by_username(data['username'])
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400
        
        # Hash password
        data['password_hash'] = generate_password_hash(data['password'])
        del data['password']
        
        # Set default values
        data['is_active'] = True
        
        # Create user
        user_id = create_user(data)
        
        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id
        })
        
    except Exception as e:
        print(f"Error in register: {e}")
        traceback.print_exc()
        return jsonify({"error": "Registration failed"}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile."""
    try:
        current_user = get_jwt_identity()
        user = get_user_by_username(current_user['username'])
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "role": user['role'],
            "department": user['department']
        })
        
    except Exception as e:
        print(f"Error in get_profile: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get profile"}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh access token using refresh token."""
    try:
        current_user = get_jwt_identity()
        
        # Create new access token
        access_token = create_access_token(
            identity=current_user,
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify({
            "access_token": access_token
        })
        
    except Exception as e:
        print(f"Error in refresh_token: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to refresh token"}), 500