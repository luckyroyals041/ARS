from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import traceback

from . import users_bp
from auth.models import get_user_by_id, get_all_users, get_users_by_role, create_user, update_user
from auth.decorators import role_required

@users_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['hod', 'principal'])
def get_users():
    """Get all users (HoD can only see faculty in their department)."""
    try:
        current_user = get_jwt_identity()
        
        # If HoD, only return faculty in their department
        if current_user['role'] == 'hod':
            users = get_users_by_role('faculty', current_user['department'])
        # If principal, return all users
        else:
            users = get_all_users()
        
        # Remove password hash from response
        for user in users:
            if 'password_hash' in user:
                del user['password_hash']
        
        return jsonify({"data": users})
        
    except Exception as e:
        print(f"Error in get_users: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get users"}), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get a specific user."""
    try:
        current_user = get_jwt_identity()
        
        # Users can only view their own profile unless they are HoD or principal
        if current_user['id'] != user_id and current_user['role'] == 'faculty':
            return jsonify({"error": "Insufficient permissions"}), 403
        
        # HoDs can only view faculty in their department
        if current_user['role'] == 'hod':
            user = get_user_by_id(user_id)
            if not user or (user['role'] == 'faculty' and user['department'] != current_user['department']):
                return jsonify({"error": "Insufficient permissions"}), 403
        
        user = get_user_by_id(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Remove password hash from response
        if 'password_hash' in user:
            del user['password_hash']
        
        return jsonify({"data": user})
        
    except Exception as e:
        print(f"Error in get_user: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get user"}), 500

@users_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['principal'])
def create_new_user():
    """Create a new user (Principal only)."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role', 'department']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Hash password
        data['password_hash'] = generate_password_hash(data['password'])
        del data['password']
        
        # Set default values
        data['is_active'] = True
        
        # Create user
        user_id = create_user(data)
        
        return jsonify({
            "message": "User created successfully",
            "user_id": user_id
        })
        
    except Exception as e:
        print(f"Error in create_new_user: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to create user"}), 500

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(['hod', 'principal'])
def update_existing_user(user_id):
    """Update an existing user."""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        # Get existing user
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # HoDs can only update faculty in their department
        if current_user['role'] == 'hod':
            if user['role'] != 'faculty' or user['department'] != current_user['department']:
                return jsonify({"error": "Insufficient permissions"}), 403
            
            # HoDs cannot change role or department
            if 'role' in data or 'department' in data:
                return jsonify({"error": "Cannot change role or department"}), 403
        
        # Handle password update
        if 'password' in data:
            data['password_hash'] = generate_password_hash(data['password'])
            del data['password']
        
        # Update user
        success = update_user(user_id, data)
        
        if not success:
            return jsonify({"error": "Failed to update user"}), 500
        
        return jsonify({
            "message": "User updated successfully"
        })
        
    except Exception as e:
        print(f"Error in update_existing_user: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to update user"}), 500

@users_bp.route('/<int:user_id>/activate', methods=['PUT'])
@jwt_required()
@role_required(['principal'])
def activate_user(user_id):
    """Activate a user (Principal only)."""
    try:
        # Get existing user
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Update user
        success = update_user(user_id, {'is_active': True})
        
        if not success:
            return jsonify({"error": "Failed to activate user"}), 500
        
        return jsonify({
            "message": "User activated successfully"
        })
        
    except Exception as e:
        print(f"Error in activate_user: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to activate user"}), 500

@users_bp.route('/<int:user_id>/deactivate', methods=['PUT'])
@jwt_required()
@role_required(['principal'])
def deactivate_user(user_id):
    """Deactivate a user (Principal only)."""
    try:
        # Get existing user
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Update user
        success = update_user(user_id, {'is_active': False})
        
        if not success:
            return jsonify({"error": "Failed to deactivate user"}), 500
        
        return jsonify({
            "message": "User deactivated successfully"
        })
        
    except Exception as e:
        print(f"Error in deactivate_user: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to deactivate user"}), 500