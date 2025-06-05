# app/services/user_service.py

from google.cloud import datastore
client = datastore.Client()

def get_all_users():
    """
    Query Datastore kind="users" (which should already have exactly nine seeded entries),
    project only "role" and "sub", and return a list of dicts:
        [ { "id": <int>, "role": <str>, "sub": <str> }, … ]
    """
    query = client.query(kind="users")
    # Only fetch "role" and "sub" properties—Datastore key holds the ID.
    query.projection = ["role", "sub"]
    entities = list(query.fetch())

    result = []
    for ent in entities:
        result.append({
            "id": ent.key.id,
            "role": ent["role"],
            "sub": ent["sub"],
        })
    return result

def get_user_by_id(user_id: int) -> dict | None:
    """
    Fetch exactly one user entity from Datastore (kind="users").
    Returns a dict with keys id, role, sub, plus avatar_url if set,
    or None if no such entity exists.
    """
    key = client.key("users", user_id)
    ent = client.get(key)
    if not ent:
        return None

    user = {
        "id": ent.key.id,
        "role": ent["role"],
        "sub": ent["sub"],
    }
    # If you’ve already stored an avatar_url in the entity, include it:
    if "avatar_url" in ent:
        user["avatar_url"] = ent["avatar_url"]
    return user
