import os
import traceback
from flask import jsonify, request
from database.mysql_data_handler import get_connection

def register_progress_tracking_routes(app):
    """Register all progress tracking report routes with the Flask app."""
    
    @app.route('/api/reports/curriculum-tracker/<reg_no>', methods=['GET'])
    def get_curriculum_tracker(reg_no):
        try:
            conn = get_connection()
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
                
            cursor = conn.cursor(dictionary=True)
            
            # Get student data
            cursor.execute("""
                SELECT 
                    registration_number AS registered_no,
                    name,
                    branch,
                    current_semester AS curr_semester
                FROM students
                WHERE registration_number = %s
            """, (reg_no,))
            
            student = cursor.fetchone()
            if not student:
                return jsonify({"error": "Student not found"}), 404
            
            # Get curriculum requirements for the student's branch
            cursor.execute("""
                SELECT 
                    cr.id,
                    cr.branch,
                    cr.semester,
                    cr.course_code,
                    c.name AS course_name,
                    cr.required_credits,
                    cr.is_mandatory,
                    cr.category
                FROM curriculum_requirements cr
                JOIN courses c ON cr.course_code = c.code
                WHERE cr.branch = %s
                ORDER BY cr.semester, cr.category, c.name
            """, (student['branch'],))
            
            all_requirements = cursor.fetchall()
            
            # Get completed courses for the student
            cursor.execute("""
                SELECT 
                    g.course_code,
                    c.name AS course_name,
                    c.credits,
                    c.semester,
                    g.grade,
                    g.grade_points,
                    g.result
                FROM grades g
                JOIN courses c ON g.course_code = c.code
                WHERE g.registration_number = %s AND g.result = 'PASS'
            """, (reg_no,))
            
            completed_courses = cursor.fetchall()
            completed_course_codes = [course['course_code'] for course in completed_courses]
            
            # Group requirements by semester
            requirements_by_semester = {}
            for req in all_requirements:
                sem = req['semester']
                if sem not in requirements_by_semester:
                    requirements_by_semester[sem] = []
                
                # Check if the course is completed
                req['completed'] = req['course_code'] in completed_course_codes
                requirements_by_semester[sem].append(req)
            
            # Calculate completion statistics
            total_required_credits = sum(req['required_credits'] for req in all_requirements)
            completed_credits = sum(course['credits'] for course in completed_courses)
            
            mandatory_requirements = [req for req in all_requirements if req['is_mandatory']]
            completed_mandatory = sum(1 for req in mandatory_requirements if req['course_code'] in completed_course_codes)
            
            # Calculate completion by category
            categories = set(req['category'] for req in all_requirements)
            category_stats = {}
            
            for category in categories:
                category_requirements = [req for req in all_requirements if req['category'] == category]
                category_completed = sum(1 for req in category_requirements if req['course_code'] in completed_course_codes)
                category_total_credits = sum(req['required_credits'] for req in category_requirements)
                category_completed_credits = sum(
                    course['credits'] for course in completed_courses 
                    if course['course_code'] in [req['course_code'] for req in category_requirements]
                )
                
                category_stats[category] = {
                    "total_courses": len(category_requirements),
                    "completed_courses": category_completed,
                    "total_credits": category_total_credits,
                    "completed_credits": category_completed_credits,
                    "completion_percentage": round((category_completed_credits / category_total_credits) * 100, 1) if category_total_credits > 0 else 0
                }
            
            # Calculate completion by semester
            semester_stats = {}
            for sem, requirements in requirements_by_semester.items():
                sem_completed = sum(1 for req in requirements if req['course_code'] in completed_course_codes)
                sem_total_credits = sum(req['required_credits'] for req in requirements)
                sem_completed_credits = sum(
                    course['credits'] for course in completed_courses 
                    if course['course_code'] in [req['course_code'] for req in requirements]
                )
                
                semester_stats[sem] = {
                    "total_courses": len(requirements),
                    "completed_courses": sem_completed,
                    "total_credits": sem_total_credits,
                    "completed_credits": sem_completed_credits,
                    "completion_percentage": round((sem_completed_credits / sem_total_credits) * 100, 1) if sem_total_credits > 0 else 0
                }
            
            # Prepare visualization data
            semester_labels = [f"Semester {sem}" for sem in sorted(semester_stats.keys())]
            completion_data = [semester_stats[sem]["completion_percentage"] for sem in sorted(semester_stats.keys())]
            
            visual_data = {
                "labels": semester_labels,
                "datasets": [
                    {
                        "label": "Completion Percentage",
                        "data": completion_data,
                        "backgroundColor": "rgba(69, 104, 220, 0.7)",
                        "borderColor": "#4568dc",
                        "borderWidth": 1
                    }
                ]
            }
            
            category_labels = list(category_stats.keys())
            category_completion = [category_stats[cat]["completion_percentage"] for cat in category_labels]
            
            category_data = {
                "labels": category_labels,
                "datasets": [
                    {
                        "label": "Completion Percentage",
                        "data": category_completion,
                        "backgroundColor": [
                            "rgba(69, 104, 220, 0.7)",
                            "rgba(176, 106, 179, 0.7)",
                            "rgba(76, 175, 80, 0.7)",
                            "rgba(255, 152, 0, 0.7)"
                        ],
                        "borderColor": [
                            "#4568dc",
                            "#b06ab3",
                            "#4caf50",
                            "#ff9800"
                        ],
                        "borderWidth": 1
                    }
                ]
            }
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "student": student,
                "requirementsBySemester": requirements_by_semester,
                "completionStats": {
                    "totalRequiredCredits": total_required_credits,
                    "completedCredits": completed_credits,
                    "creditCompletionPercentage": round((completed_credits / total_required_credits) * 100, 1) if total_required_credits > 0 else 0,
                    "totalMandatoryCourses": len(mandatory_requirements),
                    "completedMandatoryCourses": completed_mandatory,
                    "mandatoryCompletionPercentage": round((completed_mandatory / len(mandatory_requirements)) * 100, 1) if mandatory_requirements else 0
                },
                "categoryStats": category_stats,
                "semesterStats": semester_stats,
                "visualData": {
                    "semesterCompletion": visual_data,
                    "categoryCompletion": category_data
                }
            })
            
        except Exception as e:
            print(f"Error generating curriculum tracker report: {e}")
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @app.route('/api/reports/backlog-management/<reg_no>', methods=['GET'])
    def get_backlog_management(reg_no):
        try:
            conn = get_connection()
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
                
            cursor = conn.cursor(dictionary=True)
            
            # Get student data
            cursor.execute("""
                SELECT 
                    registration_number AS registered_no,
                    name,
                    branch,
                    current_semester AS curr_semester
                FROM students
                WHERE registration_number = %s
            """, (reg_no,))
            
            student = cursor.fetchone()
            if not student:
                return jsonify({"error": "Student not found"}), 404
            
            # Get backlog data
            cursor.execute("""
                SELECT 
                    bt.id,
                    bt.course_code,
                    c.name AS course_name,
                    c.credits,
                    c.semester AS course_semester,
                    bt.semester_failed,
                    bt.attempts,
                    bt.next_attempt_date,
                    bt.status
                FROM backlog_tracking bt
                JOIN courses c ON bt.course_code = c.code
                WHERE bt.registration_number = %s
                ORDER BY bt.next_attempt_date, bt.semester_failed
            """, (reg_no,))
            
            backlogs = cursor.fetchall()
            
            # Group backlogs by status
            backlogs_by_status = {
                "pending": [],
                "registered": [],
                "cleared": []
            }
            
            for backlog in backlogs:
                backlogs_by_status[backlog['status']].append(backlog)
            
            # Calculate impact on graduation
            current_semester = student['curr_semester']
            pending_backlogs = len(backlogs_by_status['pending']) + len(backlogs_by_status['registered'])
            
            # Assuming a student can clear 2 backlogs per semester
            backlog_delay_semesters = (pending_backlogs + 1) // 2
            
            # Normal graduation is after 8 semesters
            normal_graduation_semester = 8
            projected_graduation_semester = max(current_semester, normal_graduation_semester) + backlog_delay_semesters
            
            # Generate study plan recommendations
            study_plan = []
            
            # Group backlogs by next attempt date
            upcoming_backlogs = sorted(
                backlogs_by_status['pending'] + backlogs_by_status['registered'],
                key=lambda x: x['next_attempt_date'] if x['next_attempt_date'] else '9999-12-31'
            )
            
            # Create study plan for next 3 months
            for backlog in upcoming_backlogs[:5]:  # Limit to 5 backlogs for simplicity
                study_plan.append({
                    "course_code": backlog['course_code'],
                    "course_name": backlog['course_name'],
                    "priority": "High" if backlog['attempts'] > 1 else "Medium",
                    "recommendation": f"Focus on {backlog['course_name']}. This is attempt #{backlog['attempts']}."
                })
            
            # Prepare visualization data
            status_labels = ["Pending", "Registered", "Cleared"]
            status_counts = [
                len(backlogs_by_status['pending']),
                len(backlogs_by_status['registered']),
                len(backlogs_by_status['cleared'])
            ]
            
            status_data = {
                "labels": status_labels,
                "datasets": [
                    {
                        "label": "Backlog Count",
                        "data": status_counts,
                        "backgroundColor": [
                            "rgba(244, 67, 54, 0.7)",
                            "rgba(255, 152, 0, 0.7)",
                            "rgba(76, 175, 80, 0.7)"
                        ],
                        "borderColor": [
                            "#f44336",
                            "#ff9800",
                            "#4caf50"
                        ],
                        "borderWidth": 1
                    }
                ]
            }
            
            # Get attempt distribution
            attempt_counts = {}
            for backlog in backlogs:
                attempts = backlog['attempts']
                if attempts not in attempt_counts:
                    attempt_counts[attempts] = 0
                attempt_counts[attempts] += 1
            
            attempt_labels = [f"Attempt {i}" for i in sorted(attempt_counts.keys())]
            attempt_values = [attempt_counts[i] for i in sorted(attempt_counts.keys())]
            
            attempt_data = {
                "labels": attempt_labels,
                "datasets": [
                    {
                        "label": "Number of Courses",
                        "data": attempt_values,
                        "backgroundColor": "rgba(33, 150, 243, 0.7)",
                        "borderColor": "#2196f3",
                        "borderWidth": 1
                    }
                ]
            }
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "student": student,
                "backlogsByStatus": backlogs_by_status,
                "totalBacklogs": len(backlogs),
                "pendingBacklogs": pending_backlogs,
                "clearedBacklogs": len(backlogs_by_status['cleared']),
                "graduationImpact": {
                    "currentSemester": current_semester,
                    "normalGraduationSemester": normal_graduation_semester,
                    "backlogDelaySemesters": backlog_delay_semesters,
                    "projectedGraduationSemester": projected_graduation_semester
                },
                "studyPlan": study_plan,
                "visualData": {
                    "statusDistribution": status_data,
                    "attemptDistribution": attempt_data
                }
            })
            
        except Exception as e:
            print(f"Error generating backlog management report: {e}")
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @app.route('/api/reports/internship-tracking/<reg_no>', methods=['GET'])
    def get_internship_tracking(reg_no):
        try:
            conn = get_connection()
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
                
            cursor = conn.cursor(dictionary=True)
            
            # Get student data
            cursor.execute("""
                SELECT 
                    registration_number AS registered_no,
                    name,
                    branch,
                    current_semester AS curr_semester
                FROM students
                WHERE registration_number = %s
            """, (reg_no,))
            
            student = cursor.fetchone()
            if not student:
                return jsonify({"error": "Student not found"}), 404
            
            # Get internship/project data
            cursor.execute("""
                SELECT 
                    id,
                    type,
                    title,
                    organization,
                    start_date,
                    end_date,
                    credits,
                    grade,
                    grade_points,
                    status,
                    description
                FROM internship_projects
                WHERE registration_number = %s
                ORDER BY start_date DESC
            """, (reg_no,))
            
            internship_projects = cursor.fetchall()
            
            # Format dates for JSON serialization
            for item in internship_projects:
                if item['start_date']:
                    item['start_date'] = item['start_date'].isoformat()
                if item['end_date']:
                    item['end_date'] = item['end_date'].isoformat()
            
            # Group by type
            internships = [item for item in internship_projects if item['type'] == 'internship']
            projects = [item for item in internship_projects if item['type'] == 'project']
            
            # Group by status
            by_status = {
                "planned": [],
                "ongoing": [],
                "completed": []
            }
            
            for item in internship_projects:
                by_status[item['status']].append(item)
            
            # Calculate metrics
            total_credits = sum(item['credits'] for item in internship_projects if item['credits'])
            completed_credits = sum(item['credits'] for item in by_status['completed'] if item['credits'])
            
            avg_grade_points = 0
            if by_status['completed']:
                avg_grade_points = sum(item['grade_points'] for item in by_status['completed'] if item['grade_points']) / len(by_status['completed'])
            
            # Calculate skill development metrics
            skill_metrics = {
                "technical": calculate_skill_score(internship_projects, 'technical'),
                "communication": calculate_skill_score(internship_projects, 'communication'),
                "teamwork": calculate_skill_score(internship_projects, 'teamwork'),
                "problem_solving": calculate_skill_score(internship_projects, 'problem_solving'),
                "leadership": calculate_skill_score(internship_projects, 'leadership')
            }
            
            # Prepare visualization data
            status_labels = ["Planned", "Ongoing", "Completed"]
            status_counts = [
                len(by_status['planned']),
                len(by_status['ongoing']),
                len(by_status['completed'])
            ]
            
            status_data = {
                "labels": status_labels,
                "datasets": [
                    {
                        "label": "Count",
                        "data": status_counts,
                        "backgroundColor": [
                            "rgba(33, 150, 243, 0.7)",
                            "rgba(255, 152, 0, 0.7)",
                            "rgba(76, 175, 80, 0.7)"
                        ],
                        "borderColor": [
                            "#2196f3",
                            "#ff9800",
                            "#4caf50"
                        ],
                        "borderWidth": 1
                    }
                ]
            }
            
            # Prepare skill radar chart data
            skill_labels = list(skill_metrics.keys())
            skill_values = [skill_metrics[skill] for skill in skill_labels]
            
            skill_data = {
                "labels": [label.replace('_', ' ').title() for label in skill_labels],
                "datasets": [
                    {
                        "label": "Skill Development",
                        "data": skill_values,
                        "backgroundColor": "rgba(69, 104, 220, 0.2)",
                        "borderColor": "#4568dc",
                        "pointBackgroundColor": "#4568dc",
                        "pointBorderColor": "#fff",
                        "pointHoverBackgroundColor": "#fff",
                        "pointHoverBorderColor": "#4568dc"
                    }
                ]
            }
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "student": student,
                "internships": internships,
                "projects": projects,
                "byStatus": by_status,
                "metrics": {
                    "totalItems": len(internship_projects),
                    "totalCredits": total_credits,
                    "completedCredits": completed_credits,
                    "averageGradePoints": round(avg_grade_points, 2),
                    "skillMetrics": skill_metrics
                },
                "visualData": {
                    "statusDistribution": status_data,
                    "skillDevelopment": skill_data
                }
            })
            
        except Exception as e:
            print(f"Error generating internship tracking report: {e}")
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

def calculate_skill_score(internship_projects, skill_type):
    """Calculate a skill development score based on completed projects/internships."""
    # This is a simplified model - in a real system, you would have actual skill assessments
    completed_items = [item for item in internship_projects if item['status'] == 'completed']
    
    if not completed_items:
        return 0
    
    # Base score from 0-10
    base_score = min(len(completed_items) * 2, 10)
    
    # Adjust based on grades
    grade_bonus = sum(item['grade_points'] for item in completed_items if item['grade_points']) / len(completed_items)
    
    # Different skills might be weighted differently based on project/internship type
    skill_weights = {
        'technical': 1.2 if skill_type == 'technical' else 0.8,
        'communication': 1.1 if skill_type == 'communication' else 0.9,
        'teamwork': 1.0,
        'problem_solving': 1.1 if skill_type == 'problem_solving' else 0.9,
        'leadership': 0.8 if skill_type == 'leadership' else 1.0
    }
    
    # Calculate final score
    score = (base_score + grade_bonus) * skill_weights.get(skill_type, 1.0)
    
    # Normalize to 0-10 scale
    return min(round(score, 1), 10)