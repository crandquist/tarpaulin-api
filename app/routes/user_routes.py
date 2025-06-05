# app/routes/user_routes.py

from flask import Blueprint, jsonify
from app.auth.decorators import requires_auth, requires_role
from app.services.user_service import get_all_users
from app.errors.exceptions import UnauthorizedError, ForbiddenError, BadRequestError

# Create blueprint *with* url_prefix="/users"
users_bp = Blueprint('users', __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET"])
@requires_auth
@requires_role("admin")
def get_users():
    users = get_all_users()
    return jsonify(users), 200
