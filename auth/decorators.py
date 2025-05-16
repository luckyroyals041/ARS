from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def role_required(allowed_roles):
    """Decorator to check if the user has the required role."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            
            if not current_user or 'role' not in current_user:
                return jsonify({"error": "Invalid token"}), 401
            
            if current_user['role'] not in allowed_roles:
                return jsonify({"error": "Insufficient permissions"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator