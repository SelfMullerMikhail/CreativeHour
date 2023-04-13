import time
import threading

from bd_function import BdHelper
from CONSTAINS import TIME_FIRE, ADMIN_IP_MISHA, PUSHING_TIME, MORNING_MESSAGE
from  decoration import Decoration

class TimeCheker:
    def __init__(self,event,  bot) -> None:
        self.database = BdHelper("AsyaApp.db")
        self.bot = bot
        self.event = event
        
    @Decoration().decore_bd_function
    def kick_members(self, users):
        for user in users:
            try:
                self.bot.kick_members(user[3], user[0])
            except Exception as e:
                self.bot.bot.send_message(ADMIN_IP_MISHA, str(e))
                

    @Decoration().decore_bd_function
    def send_pushing(self, users_wake_up):
        for user in users_wake_up:
            try:
                self.bot.bot.send_message(user[1], MORNING_MESSAGE)
            except Exception as e:
                self.bot.bot.send_message(ADMIN_IP_MISHA, str(e))

    def time_cheker(self):
            while True:
                if time.localtime().tm_min == 18:
                    self.event.set()
                    users = self.database.get_ReadyUser_from_time(TIME_FIRE, "view_persons_in_chats")   
                    self.kick_members(users)
                    users_wake_up = self.database.get_ReadyUser_from_time(PUSHING_TIME, "ReadyUsers")
                    self.send_pushing(users_wake_up)
                time.sleep(10)