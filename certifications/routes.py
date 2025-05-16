from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback

from . import certifications_bp
from .models import (
    get_student_certifications, get_certification_by_id, create_certification,
    update_certification, verify_certification, delete_certification, get_certification_stats
)
from auth.decorators import role_required

@certifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_certifications():
    """Get all certifications or filter by student ID."""
    try:
        student_id = request.args.get('student_id', None)
        verified_only = request.args.get('verified_only', 'false').lower() == 'true'
        
        certifications = get_student_certifications(student_id, verified_only)
        
        return jsonify({"data": certifications})
        
    except Exception as e:
        print(f"Error in get_certifications: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get certifications"}), 500

@certifications_bp.route('/<int:certification_id>', methods=['GET'])
@jwt_required()
def get_certification(certification_id):
    """Get a specific certification."""
    try:
        certification = get_certification_by_id(certification_id)
        
        if not certification:
            return jsonify({"error": "Certification not found"}), 404
        
        return jsonify({"data": certification})
        
    except Exception as e:
        print(f"Error in get_certification: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get certification"}), 500

@certifications_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['faculty', 'hod', 'principal'])
def add_certification():
    """Add a new certification."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_id', 'title', 'certification_type', 'issuing_organization']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create certification
        certification_id = create_certification(data)
        
        if not certification_id:
            return jsonify({"error": "Failed to create certification"}), 500
        
        return jsonify({
            "message": "Certification created successfully",
            "certification_id": certification_id
        })
        
    except Exception as e:
        print(f"Error in add_certification: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to create certification"}), 500

@certifications_bp.route('/<int:certification_id>', methods=['PUT'])
@jwt_required()
@role_required(['faculty', 'hod', 'principal'])
def update_existing_certification(certification_id):
    """Update an existing certification."""
    try:
        data = request.get_json()
        
        # Get existing certification
        certification = get_certification_by_id(certification_id)
        if not certification:
            return jsonify({"error": "Certification not found"}), 404
        
        # Update certification
        success = update_certification(certification_id, data)
        
        if not success:
            return jsonify({"error": "Failed to update certification"}), 500
        
        return jsonify({
            "message": "Certification updated successfully"
        })
        
    except Exception as e:
        print(f"Error in update_existing_certification: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to update certification"}), 500

@certifications_bp.route('/<int:certification_id>/verify', methods=['PUT'])
@jwt_required()
@role_required(['hod', 'principal'])
def verify_existing_certification(certification_id):
    """Verify a certification."""
    try:
        current_user = get_jwt_identity()
        
        # Get existing certification
        certification = get_certification_by_id(certification_id)
        if not certification:
            return jsonify({"error": "Certification not found"}), 404
        
        # Verify certification
        success = verify_certification(certification_id, current_user['id'])
        
        if not success:
            return jsonify({"error": "Failed to verify certification"}), 500
        
        return jsonify({
            "message": "Certification verified successfully"
        })
        
    except Exception as e:
        print(f"Error in verify_existing_certification: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to verify certification"}), 500

@certifications_bp.route('/<int:certification_id>', methods=['DELETE'])
@jwt_required()
@role_required(['faculty', 'hod', 'principal'])
def delete_existing_certification(certification_id):
    """Delete a certification."""
    try:
        # Get existing certification
        certification = get_certification_by_id(certification_id)
        if not certification:
            return jsonify({"error": "Certification not found"}), 404
        
        # Delete certification
        success = delete_certification(certification_id)
        
        if not success:
            return jsonify({"error": "Failed to delete certification"}), 500
        
        return jsonify({
            "message": "Certification deleted successfully"
        })
        
    except Exception as e:
        print(f"Error in delete_existing_certification: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to delete certification"}), 500

@certifications_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['hod', 'principal'])
def get_certifications_stats():
    """Get certification statistics."""
    try:
        stats = get_certification_stats()
        
        return jsonify({"data": stats})
        
    except Exception as e:
        print(f"Error in get_certifications_stats: {e}")
        traceback.print_exc()
        return jsonify({"error": "Failed to get certification statistics"}), 500