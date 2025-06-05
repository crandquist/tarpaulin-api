# tests/test_auth.py

import json
import pytest

from app.errors.exceptions import UnauthorizedError, BadRequestError


def test_login_missing_fields(client):
    """
    POST /users/login with no JSON or missing 'username'/'password' must return 400
    and {"Error": "The request body is invalid"}.
    """
    # 1a. No JSON body at all
    resp1 = client.post("/users/login", data="")
    assert resp1.status_code == 400
    assert resp1.get_json() == {"Error": "The request body is invalid"}

    # 1b. JSON present but missing 'password'
    resp2 = client.post(
        "/users/login",
        data=json.dumps({"username": "admin@osu.com"}),
        content_type="application/json",
    )
    assert resp2.status_code == 400
    assert resp2.get_json() == {"Error": "The request body is invalid"}

    # 1c. JSON present but missing 'username'
    resp3 = client.post(
        "/users/login",
        data=json.dumps({"password": "Cheese1234!"}),
        content_type="application/json",
    )
    assert resp3.status_code == 400
    assert resp3.get_json() == {"Error": "The request body is invalid"}


def test_login_invalid_credentials(client, monkeypatch):
    """
    POST /users/login with incorrect username/password should return 401
    and {"Error": "Unauthorized"}.
    We monkeypatch login_user in the auth_routes namespace to raise UnauthorizedError.
    """
    # Patch login_user in app.routes.auth_routes to raise UnauthorizedError
    import app.routes.auth_routes as auth_routes
    monkeypatch.setattr(
        auth_routes,
        "login_user",
        lambda u, p: (_ for _ in ()).throw(UnauthorizedError("Invalid credentials"))
    )

    payload = {"username": "doesnotexist@osu.com", "password": "wrongpass"}
    resp = client.post(
        "/users/login",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 401
    assert resp.get_json() == {"Error": "Unauthorized"}


def test_login_success(client, monkeypatch):
    """
    POST /users/login with correct username/password should return 200
    and a JSON body containing exactly {"token": "<jwt>"}.
    We monkeypatch login_user in the auth_routes namespace to return a dict with 'token'.
    """
    dummy_token = "dummy.jwt.token"
    import app.routes.auth_routes as auth_routes

    # Patch login_user in auth_routes to return our dummy token
    monkeypatch.setattr(
        auth_routes,
        "login_user",
        lambda u, p: {"token": dummy_token}
    )

    payload = {"username": "admin@osu.com", "password": "Cheese1234!"}
    resp = client.post(
        "/users/login",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()

    # The response must be a JSON object with a single key "token"
    assert isinstance(data, dict)
    assert set(data.keys()) == {"token"}
    assert data["token"] == dummy_token
