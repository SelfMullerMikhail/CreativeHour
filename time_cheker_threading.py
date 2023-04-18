import time
import threading

from bd_function import BdHelper
from CONSTAINS import TIME_FIRE, PUSHING_TIME, MORNING_MESSAGE
from  decoration import Decoration

class TimeCheker:
    def __init__(self,event,  bot) -> None:
        self.database = BdHelper("AsyaApp.db")
        self.bot = bot
        self.event = event
        
    @Decoration().decore_bd_function
    def kick_members(self, users):
        for user in users:
            time.sleep(0.2)
            self.bot.kick_members(user[3], user[0])
            self.bot.unbun_members(user[3], user[0])
                

    @Decoration().decore_bd_function
    def send_pushing(self, users_wake_up):
        for user in users_wake_up:
            time.sleep(0.2)
            self.bot.try_send_message(user[1], MORNING_MESSAGE())

    def time_cheker(self):
            while True:
                self.event.set()
                users = self.database.get_ReadyUser_from_time(TIME_FIRE(), "view_persons_in_chats") 
                self.kick_members(users)
                users_wake_up = self.database.get_ReadyUser_from_time(PUSHING_TIME(), "ReadyUsers")
                self.send_pushing(users_wake_up)
                time.sleep(60)