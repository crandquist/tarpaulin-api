# app/routes/user_routes.py

from flask import Blueprint, jsonify, request
from app.auth.decorators import requires_auth, requires_role
from app.services.user_service import get_all_users
from app.utils.responses import error_response
from app.errors.exceptions import UnauthorizedError, ForbiddenError

# Make sure url_prefix is "/users"
users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET"])
@requires_auth
@requires_role("admin")
def get_users():
    """
    GET /users/
        • 401 if no or invalid JWT
        • 403 if JWT is valid but role != "admin"
        • 200 + [ {id, role, sub}, … ] if role == "admin"
    """
    try:
        users = get_all_users()
        return jsonify(users), 200
    except UnauthorizedError:
        return error_response("Unauthorized", 401)
    except ForbiddenError:
        return error_response("You don't have permission on this resource", 403)
