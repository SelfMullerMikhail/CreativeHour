import os
import datetime
from CONSTAINS import ADMIN_IP_MISHA

class Decoration:

    def _write_logs(self, info: str):
        data = os.path.join(os.getcwd(), "error_logs", "logs")
        with open(f"{data}.txt", "a") as file:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            file.write(f"{os.linesep}{time} {info}")


    def decore_bd_function(self, func):
        def wrapper(*args):
            try:
                info = func(*args)
                return info
            except Exception as e:
                print(e)
                self._write_logs(str(e))
        return wrapper