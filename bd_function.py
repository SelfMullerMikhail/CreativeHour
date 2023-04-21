import sqlite3
# from decoration import Decoration.decore_bd_function
from decoration import Decoration

class BdHelper:
    
    def __init__(self, database):
        self.database = database

    
    def user_push_start(self, user_id, user_name):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""INSERT INTO user_activity_start(user_id, user_name) VALUES({user_id}, '{user_name}')""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)

    
    def user_came(self, user_id, user_name, chat_id):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""INSERT INTO user_came(user_id, user_name, chat_id) VALUES({user_id}, '{user_name}', {chat_id})""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)

    
    def insert_new_user(self, user_id, user_name):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""INSERT OR IGNORE INTO users(user_id, user_name) VALUES({user_id}, '{user_name}');""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)

    
    def __get_cursor(self):
        try:
            conn = sqlite3.connect(self.database)
            conn.execute('PRAGMA encoding = "UTF-8"')
            cursor = conn.cursor()
            return cursor, conn
        except Exception as e:
            self.__close_cursor_and_conn(cursor, conn)
            Decoration._write_logs(str(e))
    
    def get_one_user(self, user_id):
        cursor, conn =  self.__get_cursor()
        try:
            info = cursor.execute(f"""SELECT count(user_id) 
                                        FROM ReadyUsers 
                                        WHERE user_id = {user_id}""").fetchall()[0][0]
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            if info == 0:
                return None
            return info
        
    
    def get_user_info_from_id(self, id_user):
        cursor, conn =  self.__get_cursor()
        try:
            info = cursor.execute(f"""SELECT * 
                                    FROM ReadyUsers 
                                    WHERE user_id = {id_user}""").fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return info[0]
            
    
    def get_ReadyUser_from_time(self, time_need, table):
        cursor, conn =  self.__get_cursor()
        try:
            info = cursor.execute(f"""SELECT *  
                                FROM {table}
                                WHERE strftime('%H:%M', datetime('now', time_zone || ' hours')) = '{time_need}';""").fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return info
        
    
    def delete_user(self, user_id):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""DELETE FROM ReadyUsers
                                    WHERE user_id = {user_id}""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)

    
    def dell_all_Active_Chat(self):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""DELETE FROM Active_Chat""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)

    
    def dell_all_ReadyUsers(self):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""DELETE FROM ReadyUsers""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
    
    
    def dell_all_Messages(self):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""DELETE FROM Messages""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)

    
    def add_user(self, user_id, user_name):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""INSERT INTO 
            ReadyUsers(user_id, user_name) 
            VALUES ({user_id}, '{user_name}');""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)

    
    def set_time_zone(self, user_id, time_zone):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""UPDATE ReadyUsers 
            SET time_zone = '{time_zone}' 
            WHERE user_id = {user_id}""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)

    
    def set_active_time_start(self, user_id, active_time_start):
            cursor, conn =  self.__get_cursor()
            try:
                cursor.execute(f"""UPDATE ReadyUsers 
                SET user_time_start = '{active_time_start}' 
                WHERE user_id = {user_id}""")
            except Exception as e:
                Decoration._write_logs(str(e))
            finally:
                self.__close_cursor_and_conn(cursor, conn)
    
    
    def set_active_time_end(self, user_id, active_time_end):
            cursor, conn =  self.__get_cursor()
            try:
                cursor.execute(f"""UPDATE ReadyUsers 
                SET user_time_end = '{active_time_end}' 
                WHERE user_id = {user_id}""")
            except Exception as e:
                Decoration._write_logs(str(e))
            finally:
                self.__close_cursor_and_conn(cursor, conn)

    
    def loock_user_into_chats(self, user_id):
        cursor, conn =  self.__get_cursor()
        try:
            info = cursor.execute(f"""SELECT * FROM Active_Chat WHERE id_user = {user_id}""").fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            if info == []:
                return False
            return info

      
    def get_active_users(self, start_time, end_time):
            cursor, conn =  self.__get_cursor()
            try:
                info = cursor.execute(f"""SELECT user_id, user_name, user_time_start, user_time_end, time_zone
                FROM ReadyUsers
                WHERE (ready_flag = 'True' AND(
                    ('{start_time}' <=  user_time_start AND '{end_time}' > user_time_start) OR
                    ('{start_time}' >= user_time_start AND '{end_time}' < user_time_end) OR
                    ('{start_time}'<= user_time_start AND '{end_time}' >= user_time_end) OR
                    ('{start_time}'>= user_time_start AND '{end_time}' <= user_time_end)))""").fetchall()
            except Exception as e:
                Decoration._write_logs(str(e))
            finally:
                self.__close_cursor_and_conn(cursor, conn)
                return info

     
    def change_active_status(self, user_id, status):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""UPDATE ReadyUsers SET ready_flag = '{status}' WHERE user_id = {user_id}""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None

    
    def get_match(self, start_time, end_time):
        cursor, conn =  self.__get_cursor()
        try:
            info = cursor.execute(f"""SELECT id, user_name, user_time_start, user_time_end, time_zone
            FROM ReadyUsers
            WHERE ( ('{start_time}' <=  user_time_start AND '{end_time}' > user_time_start) OR
                ('{start_time}' >= user_time_start AND '{end_time}' < user_time_end) OR
                ('{start_time}'<= user_time_start AND '{end_time}' >= user_time_end) OR
                ('{start_time}'>= user_time_start AND '{end_time}' <= user_time_end))""").fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return info

    
    def get_free_room_id(self, min_time, max_time):
        cursor, conn =  self.__get_cursor()
        try:
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
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            if info == []:
                info = [[None, 'No free rooms', "False", "False"]]
            return info[0][0], info[0][1], info[0][2], info[0][3]
    
    
    def add_chat_into_active(self, id_chat, name):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""INSERT INTO Chats (id_chat, name, max_users, users_now)
                                VALUES ({id_chat}, '{name}', 5, 0)""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None
    
    def delete_chat_from_active(self, id_chat):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""DELETE FROM Chats WHERE id_chat = '{id_chat}'""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None

    
    def update_rooms_users_count(self, id_chat, count):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""UPDATE Chats SET users_now = {count} WHERE id_chat = '{id_chat}';""")
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None
    
    
    def get_time_active_chat_users(self, id_chat):
        cursor, conn =  self.__get_cursor()
        try:
            info = cursor.execute(f"""SELECT min(user_time_start), max(user_time_end)
            FROM view_active_chats_info
            WHERE id_chat = '{id_chat}';""").fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return info[0][0], info[0][1]

    
    def update_room_info_time(self, id_chat, time, boarder):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""UPDATE Chats SET {boarder} = '{time}' WHERE id_chat = '{id_chat}'; """).fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None

    
    def dell_user_from_Active_Chat(self, id_user=None):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""DELETE FROM Active_Chat WHERE id_user = {id_user}; """)
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None

    
    def add_user_to_Active_Chat(self, id_user, id_chat):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""INSERT INTO Active_Chat (id_user, id_chat) VALUES ({id_user}, '{id_chat}'); """)
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None
    
    
    def write_messag_history(self, chat_id, user_id, message_id):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""INSERT INTO Messages (chat_id, user_id, message_id) VALUES ({chat_id}, {user_id}, {message_id}); """)
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None
    
    
    def get_messages_from_chat(self, chat_id):
        cursor, conn =  self.__get_cursor()
        try:
            messages = cursor.execute(f"""SELECT chat_id, message_id FROM Messages WHERE chat_id = {chat_id}; """).fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return messages
    
    
    def delete_chat_messages_from_user(self, chat_id):
        cursor, conn =  self.__get_cursor()
        try:
            cursor.execute(f"""DELETE FROM Messages WHERE chat_id = {chat_id}; """)
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return None
    
    
    def get_all_users(self):
        cursor, conn =  self.__get_cursor()
        try:
            users = cursor.execute(f"""SELECT user_id FROM ReadyUsers; """).fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return users
    
    
    def get_all_chats(self):
        cursor, conn =  self.__get_cursor()
        try:
            chats = cursor.execute(f"""SELECT id_chat, name FROM Chats; """).fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return chats
    
    
    def get_all_groups(self):
        cursor, conn =  self.__get_cursor()
        try:
            groups = cursor.execute(f"""SELECT * FROM Chats;""").fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return groups
    
    
    def get_user_in_chats(self, user_id):
        cursor, conn =  self.__get_cursor()
        try:
            user_info = cursor.execute(f"""SELECT * FROM view_persons_in_chats WHERE user_id = {user_id};""").fetchall()
        except Exception as e:
            Decoration._write_logs(str(e))
        finally:
            self.__close_cursor_and_conn(cursor, conn)
            return user_info
        

    Decoration.decore_bd_function
    def __close_cursor_and_conn(self, cursor, conn):
        conn.commit()
        cursor.close()
        conn.close()


        


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