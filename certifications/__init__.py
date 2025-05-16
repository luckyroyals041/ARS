from flask import Blueprint

certifications_bp = Blueprint('certifications', __name__, url_prefix='/api/certifications')

from . import routes