def test_app_exists(client):
    """
    A trivial test to confirm that the Flask application is up.
    """
    resp = client.get("/")     # You probably return 404 or a JSON message at “/”
    assert resp.status_code in (200, 404)
