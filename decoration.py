import os
import datetime
from CONSTAINS import BUCKET_NAME
from google_cloud_connector import google_cloud_connection

class Decoration:

    def _write_logs(self, info: str):
        data = "logs.txt"
        blob, temp_file = google_cloud_connection(file_config="gracefull_obj.json", 
                                                file_name = data,
                                                bucket_name=BUCKET_NAME)
        with open(f"{temp_file}", "a") as file:
            time = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            file.write(f"{os.linesep}{time} {info}")
        blob.upload_from_filename(temp_file)


    def decore_bd_function(self, func):
        def wrapper(*args):
            try:
                info = func(*args)
                return info
            except Exception as e:
                print(func, e)
                self._write_logs(str(e))
        return wrapper