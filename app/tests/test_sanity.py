# tests/test_sanity.py

def test_app_exists(client):
    """
    A trivial test to confirm that the Flask application is up.
    """
    resp = client.get("/")     # You might get 401 if "/" requires auth
    assert resp.status_code in (200, 401, 404)
