import os
import sqlite3
import pandas as pd

from decoration import Decoration
from google.cloud import storage


from google_cloud_connector import google_cloud_connection
from CONSTAINS import BUCKET_NAME


class ExelCreator():
    def __init__(self) -> None:
        self.db_name = 'Statistic.db'
    
    @Decoration.decore_bd_function
    def get_cursor(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        return conn, cursor
    
    @Decoration.decore_bd_function
    def close_cursor(self, cursor, conn):
        cursor.close()
        conn.close()
    
    @Decoration.decore_bd_function
    def get_statistic_exel(self, table_name:str, columns: list):
        
        database = self.database
        _, temp_file = google_cloud_connection(file_config="gracefull_obj.json", 
                                file_name= database,
                                bucket_name=BUCKET_NAME)
        
        with sqlite3.connect(temp_file) as conn:
            conn.execute('PRAGMA encoding = "UTF-8"')
            cursor = conn.cursor()
            try:
                info = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
                return info
            except Exception as e:
                Decoration._write_logs(str(e))
            finally:
                cursor.close()
                os.remove(temp_file)
        execute = pd.DataFrame(info, columns=columns)
        execute.to_excel(f'{table_name}.xlsx', index=False)