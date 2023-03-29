import datetime
import os


def write_logs(info: str, folder):
        data = str(os.getcwd()) + f"\\{folder}\\" + str(datetime.date.today())
        """Write info in log.txt"""
        print(f"Write_logs: {info}, folder: {folder}")
        # with open(f"{data}.txt", "a") as file:
        #     time = datetime.datetime.now().strftime("%H:%M:%S")
        #     file.write(f"\n{time} {info}")
        #     file.close()