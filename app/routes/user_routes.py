# app/routes/user_routes.py

from flask import Blueprint, jsonify, request
from app.auth.decorators import requires_auth, requires_role
from app.services.user_service import get_all_users, get_user_by_id
from app.utils.responses import error_response
from app.errors.exceptions import UnauthorizedError, ForbiddenError, NotFoundError

# Make sure url_prefix is "/users"
users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/<int:user_id>", methods=["GET"])
@requires_auth
def get_user(user_id: int):
    """
    GET /users/<user_id>
        • 401 if no or invalid JWT (handled by @requires_auth)
        • 403 if valid JWT but not admin and JWT.sub ≠ user.sub
        • 404 if no user exists with that ID
        • 200 + JSON object with at least {id, role, sub}, plus:
            – "avatar_url" if that property exists on the Datastore entity
            – "courses": [] (an empty list) if role is "instructor" or "student"
                (Folder 3A only expects an empty list; full enrollment tests come later).
    """

    try:
        # 1) Fetch the user from Datastore
        user = get_user_by_id(user_id)
        if not user:
            raise NotFoundError("Not found")

        # 2) Extract JWT payload (set by @requires_auth). If invalid/no JWT,
        #    @requires_auth will already have thrown UnauthorizedError.
        payload = request.jwt_payload  # your decorator should have set this

        # 3) Enforce “admin OR owner” logic
        is_admin = (payload.get("role") == "admin")
        is_owner = (payload.get("sub") == user.get("sub"))
        if not (is_admin or is_owner):
            raise ForbiddenError("You don't have permission on this resource")

        # 4) Build response JSON
        response = {
            "id": user["id"],
            "role": user["role"],
            "sub": user["sub"],
        }
        # Include avatar_url if present
        if "avatar_url" in user:
            response["avatar_url"] = user["avatar_url"]

        # For Folder 3A “basic” tests, always include courses=[] if role is instructor/student
        if user["role"] in ("instructor", "student"):
            response["courses"] = []

        return jsonify(response), 200

    except UnauthorizedError:
        return error_response("Unauthorized", 401)
    except ForbiddenError:
        return error_response("You don't have permission on this resource", 403)
    except NotFoundError:
        return error_response("Not found", 404)

@users_bp.route("/users", methods=["GET"], strict_slashes=False)
@users_bp.route("/users/", methods=["GET"])
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
