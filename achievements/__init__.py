from flask import Blueprint

achievements_bp = Blueprint('achievements', __name__, url_prefix='/api/achievements')

from . import routes