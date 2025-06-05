# tests/test_users.py

import pytest

def test_get_all_users_unauthenticated(client):
    """
    Without an Authorization header, GET /users/ must return 401
    with {"Error": "Unauthorized"}.
    """
    resp = client.get("/users/")
    assert resp.status_code == 401
    assert resp.get_json() == {"Error": "Unauthorized"}


def test_get_all_users_success(client, monkeypatch):
    """
    Bypassing authentication/authorization, GET /users/ returns 200
    and a list of user dicts exactly as returned by the service layer.
    We monkeypatch both decorators to be no-ops and patch get_all_users().
    """
    # 1) Monkeypatch requires_auth and requires_role to no-ops
    import app.auth.decorators as decorators
    monkeypatch.setattr(decorators, "requires_auth", lambda f: f)
    monkeypatch.setattr(
        decorators,
        "requires_role",
        lambda role: (lambda f: f),
    )

    # 2) Patch the service layer to return a dummy list of users
    import app.services.user_service as user_service
    dummy_users = [
        {"id": 1, "role": "admin",      "sub": "auth0|admin1"},
        {"id": 2, "role": "instructor", "sub": "auth0|inst1"},
        {"id": 3, "role": "student",    "sub": "auth0|stu1"},
    ]
    monkeypatch.setattr(user_service, "get_all_users", lambda: dummy_users)

    # 3) Perform the request (no headers needed, since decorators are no-ops)
    resp = client.get("/users/")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list), "Response should be a JSON list"
    assert data == dummy_users, "Response list must match exactly what the service returned"
