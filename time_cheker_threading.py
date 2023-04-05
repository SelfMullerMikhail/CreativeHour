import time
from CONSTAINS import TIME_FIRE, ADMIN_IP_MISHA, PUSHING_TIME, MORNING_MESSAGE

class TimeCheker():
    def __init__(self, database, write_logs, bot) -> None:
        self.database = database
        self.write_logs = write_logs
        self.bot = bot

    def time_cheker(self):
            while True:
                time.sleep(60)
                if time.localtime().tm_min == 0:  
                    now = time.localtime()
                    time_now = f"{now.tm_hour}:{now.tm_min}"
                    users = self.database.get_ReadyUser_from_time(time_now, TIME_FIRE)
                    for user in users:
                        if int(user[0]) != int(ADMIN_IP_MISHA):
                            self.bot.kick_members(user[3], user[0])
                    users_wake_up = self.database.get_ReadyUser_from_time(time_now, PUSHING_TIME)
                    for user in users_wake_up:
                        self.bot.send_message(user[0], MORNING_MESSAGE)