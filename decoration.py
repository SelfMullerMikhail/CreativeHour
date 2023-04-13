import os
import datetime
from CONSTAINS import ADMIN_IP_MISHA

class Decoration:
    
    def __write_logs(self, info: str):
        # data = str(os.getcwd()) + f"\\error_logs\\" + str(datetime.date.today())
        data = str(os.getcwd()) + f"\\error_logs\\logs"
        with open(f"{data}.txt", "a") as file:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            file.write(f"\n{time} {info}")

    def decore_bd_function(self, func):
        def wrapper(*args):
            try:
                info = func(*args)
                return info
            except Exception as e:
                self.__write_logs(str(e))
        return wrapper