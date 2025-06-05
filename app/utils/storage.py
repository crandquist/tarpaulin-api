from google.cloud import storage
from flask import current_app

def upload_avatar(user_id, file_stream, content_type):
    client = storage.Client()
    bucket_name = current_app.config["STORAGE_BUCKET"]
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"avatars/{user_id}")
    blob.upload_from_string(file_stream.read(), content_type=content_type)
    return blob.public_url
