import sqlite3
import pandas as pd

from decoration import decore_bd_function
from bd_function import BdHelper



class ExelCreateor():
    def __init__(self) -> None:
        self.db_name = 'Statistic.db'
    
    @decore_bd_function
    def get_cursor(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        return conn, cursor
    
    @decore_bd_function
    def close_cursor(self, cursor, conn):
        cursor.close()
        conn.close()
    
    @decore_bd_function
    def get_statistic_exel(self, table_name:str, columns: list):
        conn, cursor = self.get_cursor()
        info = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
        execute = pd.DataFrame(info, columns=columns)
        execute.to_excel(f'{table_name}.xlsx', index=False)
        self.close_cursor(cursor, conn)