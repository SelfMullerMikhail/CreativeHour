import time
from CONSTAINS import TIME_FIRE, ADMIN_IP_MISHA

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
                        self.bot.send_message(ADMIN_IP_MISHA, "TimeCheker START")
                        now = time.localtime()
                        time_now = f"{now.tm_hour}:{now.tm_min}"
                        users = self.database.get_ReadyUser_from_time(time_now, TIME_FIRE)
                        for user in users:
                            if user[0] != ADMIN_IP_MISHA:
                                try:
                                    self.bot.kick_chat_member(user[3], user[0])
                                    self.bot.unban_chat_member(chat_id= user[3], user_id=user[0])
                                    self.write_logs(f"Wire_chat_member: {user[0]}, {user[1], user[2], user[3]}", folder="fire_members_logs")    
                                except Exception as e:
                                    self.bot.send_message(ADMIN_IP_MISHA, f"Error, kick person: {e}")
                                # self.left_chat_member(user_id_=user[0], chat_id_=user[3])
                    except Exception as e:
                        print(f"Dangerous_Error, time_cheker: {e}")
                        self.bot.send_message(ADMIN_IP_MISHA, f"Dangerous_Error, time_cheker: {e}")
                        self.write_logs(f"Dangerous_Error, time_cheker: {e}", folder="error_logs")