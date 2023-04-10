import sqlite3
from decoration import decore_bd_function

class BdHelper():
    def __init__(self, database):
        self.database = database
        
    # @decore_bd_function    
    # def s_get_user(self):
    #     cursor, conn =  self.__get_cursor()
    #     info = cursor.execute("""SELECT * FROM users""")
    #     # self.__close_cursor_and_conn(cursor, conn)
    #     return info
    
    # @decore_bd_function
    # def s_get_user_push_start(self):
    #     cursor, conn =  self.__get_cursor()
    #     info = cursor.execute("""SELECT * FROM user_activity_start""")
    #     self.__close_cursor_and_conn(cursor, conn)
    #     return info

    @decore_bd_function
    def user_push_start(self, user_id, user_name):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""INSERT INTO user_activity_start(user_id, user_name) VALUES({user_id}, '{user_name}')""")
        self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def user_came(self, user_id, user_name, chat_id):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""INSERT INTO user_came(user_id, user_name, chat_id) VALUES({user_id}, '{user_name}', {chat_id})""")
        self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def insert_new_user(self, user_id, user_name):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""INSERT OR IGNORE INTO users(user_id, user_name) VALUES({user_id}, '{user_name}');""")
        self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def __get_cursor(self):
        conn = sqlite3.connect(self.database)
        conn.execute('PRAGMA encoding = "UTF-8"')
        cursor = conn.cursor()
        return cursor, conn

    @decore_bd_function
    def get_one_user(self, user_id):
        cursor, conn =  self.__get_cursor()
        info = cursor.execute(f"""SELECT count(user_id) 
                                        FROM ReadyUsers 
                                        WHERE user_id = {user_id}""").fetchall()[0][0]
        self.__close_cursor_and_conn(cursor, conn)
        if info == 0:
            return None
        return info
        
    @decore_bd_function
    def get_user_info_from_id(self, id_user):
        cursor, conn =  self.__get_cursor()
        info = cursor.execute(f"""SELECT * 
                                FROM ReadyUsers 
                                WHERE user_id = {id_user}""").fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        print(info)
        return info[0]
            

    # @decore_bd_function
    # def get_time_zone(self, user_id):
    #     cursor, conn =  self.__get_cursor()
    #     cursor.execute(f"""SELECT time_zone 
    #                             FROM ReadyUsers
    #                             WHERE user_id = {user_id}""") 
    #     info = cursor.fetchall()
    #     if info == []:
    #         info = 0
    #     self.__close_cursor_and_conn(cursor, conn)
    #     return int(info[0][0])
    

    @decore_bd_function
    def get_ReadyUser_from_time(self, time_now, time_need, table):
        cursor, conn =  self.__get_cursor()
        info = cursor.execute(f"""SELECT *
                            FROM {table}
                            WHERE time_zone + '{time_now}' = {time_need}""").fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        return info
    


    # @decore_bd_function
    # def get_info_all_users_in_chats(self):
    #     cursor, conn =  self.__get_cursor()
    #     info = cursor.execute(f"""SELECT * FROM view_persons_in_chats""").fetchall()
    #     self.__close_cursor_and_conn(cursor, conn)
    #     return info
        
    @decore_bd_function
    def delete_user(self, user_id):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""DELETE FROM ReadyUsers
                                WHERE user_id = {user_id}""")
        self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def dell_all_Active_Chat(self):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""DELETE FROM Active_Chat""")
        self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def dell_all_ReadyUsers(self):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""DELETE FROM ReadyUsers""")
        self.__close_cursor_and_conn(cursor, conn)
    
    @decore_bd_function
    def dell_all_Messages(self):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""DELETE FROM Messages""")
        self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def add_user(self, user_id, user_name):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""INSERT INTO 
            ReadyUsers(user_id, user_name) 
            VALUES ({user_id}, '{user_name}');""")
        self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def set_time_zone(self, user_id, time_zone):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""UPDATE ReadyUsers 
        SET time_zone = '{time_zone}' 
        WHERE user_id = {user_id}""")
        self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def set_active_time_start(self, user_id, active_time_start):
            cursor, conn =  self.__get_cursor()
            cursor.execute(f"""UPDATE ReadyUsers 
            SET user_time_start = '{active_time_start}' 
            WHERE user_id = {user_id}""")
            self.__close_cursor_and_conn(cursor, conn)
    
    @decore_bd_function
    def set_active_time_end(self, user_id, active_time_end):
            cursor, conn =  self.__get_cursor()
            cursor.execute(f"""UPDATE ReadyUsers 
            SET user_time_end = '{active_time_end}' 
            WHERE user_id = {user_id}""")
            self.__close_cursor_and_conn(cursor, conn)

    @decore_bd_function
    def loock_user_into_chats(self, user_id):
        cursor, conn =  self.__get_cursor()
        info = cursor.execute(f"""SELECT * FROM Active_Chat WHERE id_user = {user_id}""").fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        if info == []:
            return False
        return info

    @decore_bd_function  
    def get_active_users(self, start_time, end_time):
            cursor, conn =  self.__get_cursor()
            info = cursor.execute(f"""SELECT user_id, user_name, user_time_start, user_time_end, time_zone
            FROM ReadyUsers
            WHERE (ready_flag = 'True' AND(
                ('{start_time}' <=  user_time_start AND '{end_time}' > user_time_start) OR
                ('{start_time}' >= user_time_start AND '{end_time}' < user_time_end) OR
                ('{start_time}'<= user_time_start AND '{end_time}' >= user_time_end) OR
                ('{start_time}'>= user_time_start AND '{end_time}' <= user_time_end)))""").fetchall()
            self.__close_cursor_and_conn(cursor, conn)
            return info

    # @decore_bd_function
    # def remove_user(self, user_id):
    #     cursor, conn =  self.__get_cursor()
    #     cursor.execute(f"""DELETE FROM ReadyUsers WHERE user_id = {user_id}""")
    #     self.__close_cursor_and_conn(cursor, conn)
    #     return None

    @decore_bd_function 
    def change_active_status(self, user_id, status):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""UPDATE ReadyUsers SET ready_flag = '{status}' WHERE user_id = {user_id}""")
        self.__close_cursor_and_conn(cursor, conn)
        return None

    @decore_bd_function
    def get_match(self, start_time, end_time):
        cursor, conn =  self.__get_cursor()
        info = cursor.execute(f"""SELECT id, user_name, user_time_start, user_time_end, time_zone
        FROM ReadyUsers
        WHERE ( ('{start_time}' <=  user_time_start AND '{end_time}' > user_time_start) OR
            ('{start_time}' >= user_time_start AND '{end_time}' < user_time_end) OR
            ('{start_time}'<= user_time_start AND '{end_time}' >= user_time_end) OR
            ('{start_time}'>= user_time_start AND '{end_time}' <= user_time_end))""").fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        return info

    @decore_bd_function
    def get_free_room_id(self, min_time, max_time):
        cursor, conn =  self.__get_cursor()
        info = cursor.execute(f"""SELECT id_chat, name, min_start_time, max_end_time
        FROM Chats
        WHERE (max_users >= users_now AND(
            ('{min_time}' <=  min_start_time AND '{max_time}' > min_start_time) OR
            ('{min_time}' >= min_start_time AND '{min_time}' < max_end_time) OR
            ('{min_time}'<= min_start_time AND '{max_time}' >= max_end_time) OR
            ('{min_time}'>= min_start_time AND '{max_time}' <= max_end_time)))
            ORDER BY users_now DESC""").fetchall()
        if info == []:
            info = cursor.execute(f"""SELECT id_chat, name, min_start_time, max_end_time
        FROM Chats
        WHERE max_users >= users_now AND min_start_time = 'None' AND max_end_time = 'None'
        ORDER BY users_now DESC""").fetchall()

        self.__close_cursor_and_conn(cursor, conn)
        if info == []:
            info = [[None, 'No free rooms', "False", "False"]]
        return info[0][0], info[0][1], info[0][2], info[0][3]

        
    # @decore_bd_function
    # def upgrade_room_info_delete(self, id_chat, min_start_time, max_end_time):
    #     cursor, conn =  self.__get_cursor()
    #     cursor.execute(f"""UPDATE Chats SET min_start_time = '{min_start_time}', 
    #                                         max_end_time = '{max_end_time}' WHERE id_chat = '{id_chat}'""")
    #     self.__close_cursor_and_conn(cursor, conn)
    #     return None
    
    @decore_bd_function
    def add_chat_into_active(self, id_chat, name):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""INSERT INTO Chats (id_chat, name, max_users, users_now)
                            VALUES ({id_chat}, '{name}', 3, 0)""")
        self.__close_cursor_and_conn(cursor, conn)
        return None
    
    def delete_chat_from_active(self, id_chat):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""DELETE FROM Chats WHERE id_chat = '{id_chat}'""")
        self.__close_cursor_and_conn(cursor, conn)
        return None

    # @decore_bd_function
    # def get_time_from_chat(self, id_chat):
    #         cursor, conn =  self.__get_cursor()
    #         info = cursor.execute(f"""SELECT min(user_time_start), max(user_time_end)
    #         FROM view_active_chats_info
    #         WHERE id_chat = '{id_chat}';""").fetchall()[0]
    #         self.__close_cursor_and_conn(cursor, conn)
    #         return info[0], info[1]

    @decore_bd_function
    def update_rooms_users_count(self, id_chat, count):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""UPDATE Chats SET users_now = {count} WHERE id_chat = '{id_chat}';""")
        self.__close_cursor_and_conn(cursor, conn)
        return None
    
    @decore_bd_function
    def get_time_active_chat_users(self, id_chat):
        cursor, conn =  self.__get_cursor()
        info = cursor.execute(f"""SELECT min(user_time_start), max(user_time_end)
        FROM view_active_chats_info
        WHERE id_chat = '{id_chat}';""").fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        return info[0][0], info[0][1]

    # @decore_bd_function
    # def get_rooms_times(self, id_chat):
    #     cursor, conn =  self.__get_cursor()
    #     info = cursor.execute(f"""SELECT min_start_time, max_end_time
    #     FROM Chats
    #     WHERE id_chat = '{id_chat}';""").fetchall()
    #     self.__close_cursor_and_conn(cursor, conn)
    #     return info[0][0], info[0][1]

    @decore_bd_function
    def update_room_info_time(self, id_chat, time, boarder):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""UPDATE Chats SET {boarder} = '{time}' WHERE id_chat = '{id_chat}'; """).fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        return None

    @decore_bd_function
    def dell_user_from_Active_Chat(self, id_user=None):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""DELETE FROM Active_Chat WHERE id_user = {id_user}; """)
        self.__close_cursor_and_conn(cursor, conn)
        return None

    @decore_bd_function
    def add_user_to_Active_Chat(self, id_user, id_chat):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""INSERT INTO Active_Chat (id_user, id_chat) VALUES ({id_user}, '{id_chat}'); """)
        self.__close_cursor_and_conn(cursor, conn)
        return None
    
    # @decore_bd_function
    # def set_chats_time(self, id_chat, time_start, time_end):
    #     cursor, conn =  self.__get_cursor()
    #     cursor.execute(f"""UPDATE Chats SET min_start_time = '{time_start}', 
    #                                             max_end_time = '{time_end}'
    #                                             WHERE id_chat = '{id_chat}'; """)
    #     self.__close_cursor_and_conn(cursor, conn)
    #     return None
    
    @decore_bd_function
    def write_messag_history(self, chat_id, user_id, message_id):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""INSERT INTO Messages (chat_id, user_id, message_id) VALUES ({chat_id}, {user_id}, {message_id}); """)
        self.__close_cursor_and_conn(cursor, conn)
        return None
    
    @decore_bd_function
    def get_messages_from_chat(self, chat_id):
        cursor, conn =  self.__get_cursor()
        messages = cursor.execute(f"""SELECT chat_id, message_id FROM Messages WHERE chat_id = {chat_id}; """).fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        return messages
    
    @decore_bd_function
    def delete_chat_messages_from_user(self, chat_id):
        cursor, conn =  self.__get_cursor()
        cursor.execute(f"""DELETE FROM Messages WHERE chat_id = {chat_id}; """)
        self.__close_cursor_and_conn(cursor, conn)
        return None
    
    @decore_bd_function
    def get_all_users(self):
        cursor, conn =  self.__get_cursor()
        users = cursor.execute(f"""SELECT user_id FROM ReadyUsers; """).fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        return users
    
    @decore_bd_function
    def get_all_chats(self):
        cursor, conn =  self.__get_cursor()
        chats = cursor.execute(f"""SELECT id_chat, name FROM Chats; """).fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        return chats
    
    @decore_bd_function
    def get_all_groups(self):
        cursor, conn =  self.__get_cursor()
        groups = cursor.execute(f"""SELECT * FROM Chats;""").fetchall()
        self.__close_cursor_and_conn(cursor, conn)
        return groups

    @decore_bd_function
    def __close_cursor_and_conn(self, cursor, conn):
        conn.commit()
        cursor.close()
        conn.close()


        


if __name__ == "__main__":
        a = BdHelper("AsyaApp.db")
        # print(a.get_match('02:00', '20:00'), "True")
        # print(a.get_match('09:00', '11:00'), "True")
        # print(a.get_match('10:00', '12:00'), "True")
        # print(a.get_match('09:00', '12:00'), "True")
        # print(a.get_match('17:00:00', '18:00:00'), "True")
        # print(a.get_match('18:00', '19:00'), "False")
        # print(a.get_match('16:00', '17:00'), "False")
        # print(a.get_free_room_id('11:00', '12:00'), "True")
        # print(a.get_free_room_id('10:00', '14:00'))
        # print(a.get_ReadyUser_from_time('12:30', '10'))
        # info = a.get_free_room_id(0, 0)
        # print(info[3] == "None")
        a.dell_user_from_Active_Chat(402816936)