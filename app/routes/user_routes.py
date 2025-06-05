# app/routes/user_routes.py

from flask import Blueprint, jsonify, request
from app.auth.decorators import requires_auth, requires_role
from app.services.user_service import get_all_users, get_user_by_id
from app.utils.responses import error_response
from app.errors.exceptions import UnauthorizedError, ForbiddenError, NotFoundError
from app.models.user import User

# Make sure url_prefix is "/users"
users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/<int:user_id>", methods=["GET"])
@requires_auth
def get_user(user_id: int):
    try:
        user = get_user_by_id(user_id)
        if not user:
            raise NotFoundError("Not found")

        caller: User = request.current_user
        is_admin = (caller.role == "admin")
        is_owner = (caller.sub == user["sub"])
        if not (is_admin or is_owner):
            raise ForbiddenError("You don't have permission on this resource")

        response = {
            "id":   user["id"],
            "role": user["role"],
            "sub":  user["sub"],
        }
        if "avatar_url" in user:
            response["avatar_url"] = user["avatar_url"]
        if user["role"] in ("instructor", "student"):
            response["courses"] = []
        return jsonify(response), 200

    except UnauthorizedError:
        return error_response("Unauthorized", 401)
    except ForbiddenError:
        return error_response("You don't have permission on this resource", 403)
    except NotFoundError:
        return error_response("Not found", 404)


@users_bp.route("", methods=["GET"])
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
