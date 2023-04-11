import time
import threading
from loger import write_logs
from bd_function import BdHelper
from CONSTAINS import TIME_FIRE, ADMIN_IP_MISHA, PUSHING_TIME, MORNING_MESSAGE

class TimeCheker():
    def __init__(self, bot) -> None:
        self.database = BdHelper("AsyaApp.db")
        self.write_logs = write_logs
        self.bot = bot

    def time_cheker(self):
            while True:
                try:
                    if time.localtime().tm_min == 0:  
                        users = self.database.get_ReadyUser_from_time(TIME_FIRE, "view_persons_in_chats")
                        for user in users:
                            if int(user[0]) != int(ADMIN_IP_MISHA):
                                threading.Thread(target=self.bot.kick_members, args=(user[3], user[0])).start()
                        users_wake_up = self.database.get_ReadyUser_from_time(PUSHING_TIME, "ReadyUsers")
                        for user in users_wake_up:
                            try:
                                threading.Thread(target=self.bot.bot.send_message, args=(user[1], MORNING_MESSAGE)).start()
                            except Exception as e:
                                self.bot.bot.send_message(ADMIN_IP_MISHA, str(e))
                    time.sleep(60)
                except Exception as e:
                    self.bot.bot.send_message(ADMIN_IP_MISHA, str(e))