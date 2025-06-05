from google.cloud import datastore
from app.errors.exceptions import NotFoundError

client = datastore.Client()

def get_all_users():
    query = client.query(kind="users")
    # Only project id, role, sub so no extra fields come back
    query.projection = ["id", "role", "sub"]
    entities = list(query.fetch())
    result = []
    for ent in entities:
        result.append({
            "id": ent.key.id,
            "role": ent["role"],
            "sub": ent["sub"]
        })
    return result
