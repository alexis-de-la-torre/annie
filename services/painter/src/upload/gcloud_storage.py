import os

from gcloud import storage


def upload_img(img, name):
    if not os.path.exists("out"):
        os.makedirs("out")

    bucket = os.environ['BUCKET']

    file_name = f"{name}.jpg"

    img.save(f"out/{file_name}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(f"out/{file_name}")

    return f"https://storage.googleapis.com/{bucket}/{file_name}"