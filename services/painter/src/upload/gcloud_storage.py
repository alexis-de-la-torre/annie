import os

from gcloud import storage

def upload_img(img, name):
    if not os.path.exists("out"):
        os.makedirs("out")

    bucket_name = os.environ['BUCKET']

    name = name.replace(" ", "-").replace("+", "-")

    file_name = f"{name}.jpg"

    file_name = file_name.replace(" ", "-").replace("+", "-")

    img.save(f"out/{file_name}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(f"out/{file_name}")

    return f"https://storage.googleapis.com/{bucket_name}/{file_name}"