from google.cloud import storage


def google_cloud_connection(file_config:str, bucket_name:str, file_name:str):
    client = storage.Client.from_service_account_json(file_config)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_name)
    blob.download_to_filename(file_name)
    return blob, file_name