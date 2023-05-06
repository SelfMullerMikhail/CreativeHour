import json
import os

from decoration import Decoration
from google_cloud_connector import google_cloud_connection

from CONSTAINS import BUCKET_NAME

class ConfigFiles:
    def __init__(self):
        ...
    
    @classmethod
    def gracefull_create(self):
        
        self.obj = {
            "type": "service_account",
            "project_id": "graceful-byway-385815",
            "client_email": "creative-houre-servise-account@graceful-byway-385815.iam.gserviceaccount.com",
            "client_id": "112172202864725306768",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/creative-houre-servise-account%40graceful-byway-385815.iam.gserviceaccount.com"
                }
        self.__privat_key = os.getenv("private_key")
        self.obj["private_key_id"] = os.getenv("private_key_id")
        self.obj["private_key"] = f"-----BEGIN PRIVATE KEY-----{self.__privat_key}\n-----END PRIVATE KEY-----\n",
        with open("gracefull_obj.json", "w") as f:
            json.dump(self.obj, f)
        return self.obj
            
    @classmethod
    def constants_create(self):
        try:
            google_cloud_connection(file_config="gracefull_obj.json",
                                    file_name="CONSTANT.json",
                                    bucket_name=BUCKET_NAME)
        except Exception as e:
            Decoration._write_logs(e)
            
if __name__ == "__main__":
    ConfigFiles.gracefull_create()
