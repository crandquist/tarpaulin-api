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
