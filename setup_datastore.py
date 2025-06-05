#!/usr/bin/env python3
"""
setup_datastore.py

Populate Google Cloud Datastore with nine users (1 admin, 2 instructors, 6 students).
Each entity has exactly three properties: id (auto-generated), sub (empty string for now), and role.
After running this, you’ll use Postman (and your POST /users/:id endpoint) to set each user’s `sub` value
to the Auth0-issued subject (sub) from the JWT. 
"""

import os
from google.cloud import datastore

# If you are using the Datastore emulator, ensure these environment variables are set:
#   export DATASTORE_EMULATOR_HOST="localhost:8081"
#   export DATASTORE_PROJECT_ID="your-test-project-id"
#
# Otherwise, the script will use your GCP project configured in GOOGLE_CLOUD_PROJECT.

def main():
    # Instantiate the Datastore client (will pick up emulator if env var is set)
    client = datastore.Client()

    # Kind name for user entities
    kind = "users"

    # First, optionally clear out any existing users in this kind
    # (Warning: This deletes *all* entities of kind "users" in the configured project/emulator)
    query = client.query(kind=kind)
    query.keys_only()
    existing = list(query.fetch())
    if existing:
        print(f"Deleting {len(existing)} existing '{kind}' entities...")
        keys_to_delete = [entity.key for entity in existing]
        client.delete_multi(keys_to_delete)

    # Define the nine users to create. We leave 'sub' blank; Postman will fill it in later.
    to_insert = [
        {"role": "admin",      "sub": ""},
        {"role": "instructor", "sub": ""},
        {"role": "instructor", "sub": ""},
        {"role": "student",    "sub": ""},
        {"role": "student",    "sub": ""},
        {"role": "student",    "sub": ""},
        {"role": "student",    "sub": ""},
        {"role": "student",    "sub": ""},
        {"role": "student",    "sub": ""},
    ]

    print(f"Inserting {len(to_insert)} '{kind}' entities...")

    for user_data in to_insert:
        key = client.key(kind)
        entity = datastore.Entity(key=key)
        entity.update({
            "role": user_data["role"],
            "sub": user_data["sub"],
        })
        client.put(entity)
        print(f"  • Created User id={entity.key.id} role={entity['role']} sub='{entity['sub']}'")

    print("Datastore seeding complete. You should now have exactly nine 'users' entities.")
    print("Next, run your Flask app and use Postman’s tests to populate each user’s `sub` property with the Auth0 JWT subject.")

if __name__ == "__main__":
    main()
