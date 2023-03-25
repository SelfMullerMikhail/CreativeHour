import time

class TimeCheker():
    def __init__(self, database, write_logs, bot, left_chat_member) -> None:
        self.database = database
        self.write_logs = write_logs
        self.bot = bot
        self.left_chat_member = left_chat_member

    def time_cheker(self):
        try:
            while True:
                now = time.localtime()
                time_now = f"{now.tm_hour}:{now.tm_min}"
                users = self.database.get_ReadyUser_from_time(time_now, 5)
                for user in users:
                    self.bot.kick_chat_member(chat_id=user[0], user_id=user[3])
                    self.left_chat_member(user_id_=user[0], chat_id_=user[3])
                    self.write_logs(f"Wire_chat_member: {user[0]}, {user[1], user[2], user[3]}", folder="fire_members_logs")
                time.sleep(60*60)
        except Exception as e:
            self.bot.send_message(243980106, f"Dangerous_Error, time_cheker: {e}")
            self.write_logs(f"Dangerous_Error, time_cheker: {e}", folder="error_logs")