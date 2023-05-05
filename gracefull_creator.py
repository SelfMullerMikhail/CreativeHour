import json
import os
from google.cloud import storage
from google_cloud_connector import google_cloud_connection

from CONSTAINS import BUCKET_NAME

class ConfigFiles:
    def __init__(self):
        self.obj = {}
    
    def gracefull_create(self):
        self.obj["type"] = os.getenv('service_account')
        self.obj["project_id"] = os.getenv("project_id")
        self.obj["private_key_id"] = os.getenv("private_key_id")
        self.obj["private_key"] = os.getenv("private_key")
        self.obj["client_email"] = os.getenv("client_email")
        self.obj["client_id"] = os.getenv("client_id")
        self.obj["auth_uri"] = os.getenv("auth_uri")
        self.obj["token_uri"] = os.getenv("token_uri")
        self.obj["auth_provider_x509_cert_url"] = (
            os.getenv("auth_provider_x509_cert_url"))
        self.obj["client_x509_cert_url"] = os.getenv("client_x509_cert_url")
        with open("gracefull_obj.json", "w") as f:
            json.dump(self.obj, f)
            
    def constants_create(self):
        google_cloud_connection(file_config="gracefull_obj.json",
                                file_name="CONSTANT.json",
                                bucket_name=BUCKET_NAME)
        
