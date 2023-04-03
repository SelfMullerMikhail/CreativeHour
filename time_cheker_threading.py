import time
from CONSTAINS import TIME_FIRE, ADMIN_IP_MISHA, PUSHING_TIME, MORNING_MESSAGE

class TimeCheker():
    def __init__(self, database, write_logs, bot, left_chat_member) -> None:
        self.database = database
        self.write_logs = write_logs
        self.bot = bot
        self.left_chat_member = left_chat_member

    def time_cheker(self):
            while True:
                time.sleep(60)
                if time.localtime().tm_min == 0:
                    try:    
                        now = time.localtime()
                        time_now = f"{now.tm_hour}:{now.tm_min}"
                        users = self.database.get_ReadyUser_from_time(time_now, TIME_FIRE)
                        self.bot.bot_send_message(ADMIN_IP_MISHA, f"Time_cheker: {time_now}")
                        for user in users:
                            self.bot.send_message(ADMIN_IP_MISHA, f"Time_cheker: {user[0]}, {user[1]}")
                            if int(user[0]) != int(ADMIN_IP_MISHA):
                                try:
                                    self.bot.send_message(ADMIN_IP_MISHA, f"Time_cheker: kick: {user[1]}")
                                except:
                                    ...
                                try:
                                    self.bot.kick_chat_member(user[3], user[0])
                                    self.bot.unban_chat_member(chat_id= user[3], user_id=user[0])  
                                    self.bot.send_message(ADMIN_IP_MISHA, f"{user[1]} was kick")
                                except Exception as e:
                                    self.bot.send_message(ADMIN_IP_MISHA, f"Error, kick person: {e}")
                                # self.left_chat_member(user_id_=user[0], chat_id_=user[3])
                        try:
                            users_wake_up = self.database.get_ReadyUser_from_time(time_now, PUSHING_TIME)
                            for user in users_wake_up:
                                self.bot.send_message(user[0], MORNING_MESSAGE)
                        except:
                            self.bot.send_message(ADMIN_IP_MISHA, f"Wrong push message{user[1]}")
                    except Exception as e:
                        self.bot.send_message(ADMIN_IP_MISHA, f"Dangerous_Error, time_cheker: {e}")