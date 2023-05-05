import os
import sqlite3
from decoration import Decoration

from functools import wraps
from google_cloud_connector import google_cloud_connection

from CONSTAINS import BUCKET_NAME

def with_cursor(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        database = self.database
        blob, temp_file = google_cloud_connection(file_config="gracefull_obj.json",
                                bucket_name=BUCKET_NAME,
                                file_name=database)
        
        with sqlite3.connect(temp_file) as conn:
            conn.execute('PRAGMA encoding = "UTF-8"')
            cursor = conn.cursor()
            try:
                func = method(self, cursor, *args, **kwargs)
                conn.commit()
                blob.upload_from_filename(temp_file)
            except Exception as e:
                Decoration._write_logs(str(e))
            finally:
                cursor.close()
        try:
            conn.close()
            os.remove(temp_file)
        except Exception as e:
            Decoration._write_logs(e)
        finally:
            return func
    return wrapper

class BdHelper:
    
    def __init__(self, database):
        self.database = database
    
    @with_cursor
    def user_push_start(self, cursor, user_id, user_name):
        cursor.execute(f"""INSERT INTO user_activity_start(user_id, user_name) VALUES({user_id}, '{user_name}')""")
    
    @with_cursor
    def user_came(self, cursor, user_id, user_name, chat_id):
        cursor.execute(f"""INSERT INTO user_came(user_id, user_name, chat_id) VALUES({user_id}, '{user_name}', {chat_id})""")

    @with_cursor
    def insert_new_user(self, cursor, user_id, user_name):
        cursor.execute(f"""INSERT OR IGNORE INTO users(user_id, user_name) VALUES({user_id}, '{user_name}');""")
        
    @with_cursor
    def get_one_user(self, cursor, user_id):
        info = cursor.execute(f"""SELECT count(user_id) 
                                        FROM ReadyUsers 
                                        WHERE user_id = {user_id}""").fetchall()[0][0]
        if info == 0:
            return None
        return info
        
    @with_cursor
    def get_user_info_from_id(self, cursor, id_user):
        info = cursor.execute(f"""SELECT * 
                                FROM ReadyUsers 
                                WHERE user_id = {id_user}""").fetchall()
        return info[0]
            
    @with_cursor
    def get_ReadyUser_from_time(self, cursor, time_need, table):
        info = cursor.execute(f"""SELECT *  
                                FROM {table}
                                WHERE strftime('%H:%M', datetime('now', time_zone || ' hours')) = '{time_need}';""").fetchall()
        return info
        
    @with_cursor
    def delete_user(self, cursor, user_id):
            cursor.execute(f"""DELETE FROM ReadyUsers
                                    WHERE user_id = {user_id}""")

    @with_cursor
    def dell_all_Active_Chat(self, cursor):
        cursor.execute(f"""DELETE FROM Active_Chat""")

    @with_cursor
    def dell_all_ReadyUsers(self, cursor):
        cursor.execute(f"""DELETE FROM ReadyUsers""")
    
    @with_cursor
    def dell_all_Messages(self, cursor):
            cursor.execute(f"""DELETE FROM Messages""")
            
    @with_cursor    
    def add_user(self, cursor, user_id, user_name):
        cursor.execute(f"""INSERT INTO 
            ReadyUsers(user_id, user_name) 
            VALUES ({user_id}, '{user_name}');""")

    @with_cursor
    def set_time_zone(self, cursor, user_id, time_zone):
        cursor.execute(f"""UPDATE ReadyUsers 
            SET time_zone = '{time_zone}' 
            WHERE user_id = {user_id}""")

    @with_cursor
    def set_active_time_start(self, cursor, user_id, active_time_start):
        cursor.execute(f"""UPDATE ReadyUsers 
                SET user_time_start = '{active_time_start}' 
                WHERE user_id = {user_id}""")
    
    @with_cursor
    def set_active_time_end(self, cursor, user_id, active_time_end):
        cursor.execute(f"""UPDATE ReadyUsers 
                SET user_time_end = '{active_time_end}' 
                WHERE user_id = {user_id}""")
    
    @with_cursor
    def loock_user_into_chats(self, cursor, user_id):
        info = cursor.execute(f"""SELECT * FROM Active_Chat WHERE id_user = {user_id}""").fetchall()
        if info == []:
            return False
        return info

    @with_cursor
    def get_active_users(self, cursor, start_time, end_time):
        info = cursor.execute(f"""SELECT user_id, user_name, user_time_start, user_time_end, time_zone
                FROM ReadyUsers
                WHERE (ready_flag = 'True' AND(
                    ('{start_time}' <=  user_time_start AND '{end_time}' > user_time_start) OR
                    ('{start_time}' >= user_time_start AND '{end_time}' < user_time_end) OR
                    ('{start_time}'<= user_time_start AND '{end_time}' >= user_time_end) OR
                    ('{start_time}'>= user_time_start AND '{end_time}' <= user_time_end)))""").fetchall()
        return info

    @with_cursor
    def change_active_status(self, cursor, user_id, status):
        cursor.execute(f"""UPDATE ReadyUsers SET ready_flag = '{status}' WHERE user_id = {user_id}""")
        return None

    @with_cursor
    def get_match(self, cursor, start_time, end_time):
        info = cursor.execute(f"""SELECT id, user_name, user_time_start, user_time_end, time_zone
            FROM ReadyUsers
            WHERE ( ('{start_time}' <=  user_time_start AND '{end_time}' > user_time_start) OR
                ('{start_time}' >= user_time_start AND '{end_time}' < user_time_end) OR
                ('{start_time}'<= user_time_start AND '{end_time}' >= user_time_end) OR
                ('{start_time}'>= user_time_start AND '{end_time}' <= user_time_end))""").fetchall()
        return info

    @with_cursor
    def get_free_room_id_max_min(self, cursor, min_time, max_time):
        info = cursor.execute(f"""SELECT id_chat, name, min_start_time, max_end_time
            FROM Chats
            WHERE (max_users >= users_now AND(
                ('{min_time}' <=  min_start_time AND '{max_time}' > min_start_time) OR
                ('{min_time}' >= min_start_time AND '{min_time}' < max_end_time) OR
                ('{min_time}'<= min_start_time AND '{max_time}' >= max_end_time) OR
                ('{min_time}'>= min_start_time AND '{max_time}' <= max_end_time)))
                ORDER BY users_now DESC""").fetchall()
        return info
            
    @with_cursor
    def get_free_room_all(self, cursor):
        info = cursor.execute(f"""SELECT id_chat, name, min_start_time, max_end_time
            FROM Chats
            WHERE max_users >= users_now AND min_start_time = 'None' AND max_end_time = 'None'
            ORDER BY users_now DESC""").fetchall()
        return info
            
    
    @with_cursor
    def add_chat_into_active(self, cursor, id_chat, name):
        cursor.execute(f"""INSERT INTO Chats (id_chat, name, max_users, users_now)
                            VALUES ({id_chat}, '{name}', 5, 0)""")
        return None
    
    @with_cursor
    def delete_chat_from_active(self, cursor, id_chat):
        cursor.execute(f"""DELETE FROM Chats WHERE id_chat = '{id_chat}'""")
        return None

    @with_cursor
    def update_rooms_users_count(self, cursor, id_chat, count):
        cursor.execute(f"""UPDATE Chats SET users_now = {count} WHERE id_chat = '{id_chat}';""")
        return None
    
    @with_cursor
    def get_time_active_chat_users(self, cursor, id_chat):
        info = cursor.execute(f"""SELECT min(user_time_start), max(user_time_end)
            FROM view_active_chats_info
            WHERE id_chat = '{id_chat}';""").fetchall()
        return info[0][0], info[0][1]

    @with_cursor
    def update_room_info_time(self, cursor, id_chat, time, boarder):
        cursor.execute(f"""UPDATE Chats SET {boarder} = '{time}' WHERE id_chat = '{id_chat}'; """).fetchall()
        return None

    @with_cursor
    def dell_user_from_Active_Chat(self, cursor, id_user=None):
        cursor.execute(f"""DELETE FROM Active_Chat WHERE id_user = {id_user}; """)
        return None

    @with_cursor
    def add_user_to_Active_Chat(self, cursor, id_user, id_chat):
        cursor.execute(f"""INSERT INTO Active_Chat (id_user, id_chat) VALUES ({id_user}, '{id_chat}'); """)
        return None
    
    @with_cursor
    def write_messag_history(self, cursor, chat_id, user_id, message_id):
        cursor.execute(f"""INSERT INTO Messages (chat_id, user_id, message_id) VALUES ({chat_id}, {user_id}, {message_id}); """)
        return None
    
    @with_cursor
    def get_messages_from_chat(self, cursor, chat_id):
        messages = cursor.execute(f"""SELECT chat_id, message_id FROM Messages WHERE chat_id = {chat_id}; """).fetchall()
        return messages
    
    @with_cursor
    def delete_chat_messages_from_user(self, cursor, chat_id):
        cursor.execute(f"""DELETE FROM Messages WHERE chat_id = {chat_id}; """)
        return None
    
    @with_cursor
    def get_all_users(self, cursor):
        users = cursor.execute(f"""SELECT user_id FROM ReadyUsers; """).fetchall()
        return users
    
    @with_cursor
    def get_all_chats(self, cursor):
        chats = cursor.execute(f"""SELECT id_chat, name FROM Chats; """).fetchall()
        return chats
    
    @with_cursor
    def get_all_groups(self, cursor):
        groups = cursor.execute(f"""SELECT * FROM Chats;""").fetchall()
        return groups
    
    @with_cursor
    def get_user_in_chats(self, cursor, user_id):
        user_info = cursor.execute(f"""SELECT * FROM view_persons_in_chats WHERE user_id = {user_id};""").fetchall()
        return user_info
        
    def get_free_room_id(self, min_time, max_time):
        info = self.get_free_room_id_max_min(min_time, max_time)
        if info == []:
            info = self.get_free_room_all()
        if info == []:
            info = [[None, 'No free rooms', "False", "False"]]
            return info[0][0], info[0][1], info[0][2], info[0][3]


        


if __name__ == "__main__":
        a = BdHelper("AsyaApp.db")
        # print(a.get_active_users('2023-04-13 20:00', '2023-04-14 00:00'), "True")
        print(a.get_active_users('2023-04-21 07:00', '2023-04-21 09:00'))
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
        # a.dell_user_from_Active_Chat(402816936)