from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback

from . import achievements_bp
from .models import (
    get_student_achievements, get_achievement_by_id, create_achievement,
    update_achievement, verify_achievement, delete_achievement, get_achievement_stats
)
from auth.decorators import role_required

@achievements_bp.route('/', methods=['GET'])
@jwt_required()
def get_achievements():
    """Get all achievements or filter by student ID."""
    try:
        student_id = request.args.get('student_id', None)
        verified_only = request.args.get('verified_only', 'false').lower() == 'true'
        
        achievements = get_student_achievements(student_id, verified_only)
        
        return jsonify({"data": achievements})
        
    except Exception as e:
        print(f"Error in get_achievements: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get achievements"}), 500

@achievements_bp.route('/<int:achievement_id>', methods=['GET'])
@jwt_required()
def get_achievement(achievement_id):
    """Get a specific achievement."""
    try:
        achievement = get_achievement_by_id(achievement_id)
        
        if not achievement:
            return jsonify({"error": "Achievement not found"}), 404
        
        return jsonify({"data": achievement})
        
    except Exception as e:
        print(f"Error in get_achievement: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get achievement"}), 500

@achievements_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['faculty', 'hod', 'principal'])
def add_achievement():
    """Add a new achievement."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_id', 'title', 'achievement_type']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create achievement
        achievement_id = create_achievement(data)
        
        if not achievement_id:
            return jsonify({"error": "Failed to create achievement"}), 500
        
        return jsonify({
            "message": "Achievement created successfully",
            "achievement_id": achievement_id
        })
        
    except Exception as e:
        print(f"Error in add_achievement: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to create achievement"}), 500

@achievements_bp.route('/<int:achievement_id>', methods=['PUT'])
@jwt_required()
@role_required(['faculty', 'hod', 'principal'])
def update_existing_achievement(achievement_id):
    """Update an existing achievement."""
    try:
        data = request.get_json()
        
        # Get existing achievement
        achievement = get_achievement_by_id(achievement_id)
        if not achievement:
            return jsonify({"error": "Achievement not found"}), 404
        
        # Update achievement
        success = update_achievement(achievement_id, data)
        
        if not success:
            return jsonify({"error": "Failed to update achievement"}), 500
        
        return jsonify({
            "message": "Achievement updated successfully"
        })
        
    except Exception as e:
        print(f"Error in update_existing_achievement: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to update achievement"}), 500

@achievements_bp.route('/<int:achievement_id>/verify', methods=['PUT'])
@jwt_required()
@role_required(['hod', 'principal'])
def verify_existing_achievement(achievement_id):
    """Verify an achievement."""
    try:
        current_user = get_jwt_identity()
        
        # Get existing achievement
        achievement = get_achievement_by_id(achievement_id)
        if not achievement:
            return jsonify({"error": "Achievement not found"}), 404
        
        # Verify achievement
        success = verify_achievement(achievement_id, current_user['id'])
        
        if not success:
            return jsonify({"error": "Failed to verify achievement"}), 500
        
        return jsonify({
            "message": "Achievement verified successfully"
        })
        
    except Exception as e:
        print(f"Error in verify_existing_achievement: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to verify achievement"}), 500

@achievements_bp.route('/<int:achievement_id>', methods=['DELETE'])
@jwt_required()
@role_required(['faculty', 'hod', 'principal'])
def delete_existing_achievement(achievement_id):
    """Delete an achievement."""
    try:
        # Get existing achievement
        achievement = get_achievement_by_id(achievement_id)
        if not achievement:
            return jsonify({"error": "Achievement not found"}), 404
        
        # Delete achievement
        success = delete_achievement(achievement_id)
        
        if not success:
            return jsonify({"error": "Failed to delete achievement"}), 500
        
        return jsonify({
            "message": "Achievement deleted successfully"
        })
        
    except Exception as e:
        print(f"Error in delete_existing_achievement: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to delete achievement"}), 500

@achievements_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['hod', 'principal'])
def get_achievements_stats():
    """Get achievement statistics."""
    try:
        stats = get_achievement_stats()
        
        return jsonify({"data": stats})
        
    except Exception as e:
        print(f"Error in get_achievements_stats: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get achievement statistics"}), 500