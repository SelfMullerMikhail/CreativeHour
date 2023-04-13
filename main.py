import datetime as dt
import re
import telebot
import time
import threading
from telebot import types
import os

from bd_function import BdHelper
from exel_statistic import ExelCreator
from CONSTAINS import *
from time_cheker_threading import TimeCheker
from decoration import Decoration


class CreativeHour:
    def __init__(self, API, event):
        super().__init__()
        self.event =event
        self.exel_creator = ExelCreator()
        self.data_base = BdHelper('AsyaApp.db')
        self.data_base_statistic = BdHelper('Statistic.db')
        self.start_message_id = {}
        self.bot = telebot.TeleBot(API)
        
    def check_event(self):
        if self.event.is_set():
            self.event.clear()
            time.sleep(1)
            
    def kick_members(self, chat_id:int, user_id:int):
        self.bot.kick_chat_member(chat_id=chat_id, user_id= user_id)
        self.bot.unban_chat_member(chat_id=chat_id, user_id= user_id)
            
    def already_in_group(self, message, markup):
        self.bot.send_message(ADMIN_IP_MISHA, f"{message.from_user.id} already in group")
        self.bot.send_message(message.from_user.id, ALREADY_IN_GROUP_TEXT, reply_markup=markup)
        
    def upgrade_room_info_time(self, id_chat):
        min_time, max_time = self.data_base.get_time_active_chat_users(id_chat)
        self.data_base.update_room_info_time(id_chat, min_time, 'min_start_time')
        self.data_base.update_room_info_time(id_chat, max_time, 'max_end_time')
        return None

    def dell_all(self):
            users = self.data_base.get_all_users()
            chats = self.data_base.get_all_chats()
            for chat in chats:
                for user in users:
                    self.kick_members(chat[0], user[0])
            self.data_base.dell_all_ReadyUsers()
            self.data_base.dell_all_Active_Chat()
            self.data_base.dell_all_Messages()

    def get_match(self, message):
        return re.search(r'Set time zone ([-+]\d) UTC', message.text)   


    def set_active_time_text(self, message, markup):
            self.bot.send_message(message.from_user.id, SET_ACTIVE_TIME_TEXT, reply_markup=markup)

    def pin_first_message(self, chat_id):
            first_message = self.bot.send_message(chat_id=chat_id, text=FIRST_MESSAGE_GROUP)
            self.bot.pin_chat_message(chat_id=chat_id, message_id=first_message.message_id)

    def send_links_to_users(self, active_users, link, markup):
        for user in active_users:
            print(user)
            try:
                time.sleep(0.5)
                self.bot.send_message(ADMIN_IP_MISHA, f"Send link to {user[2]}")
                self.bot.send_message(user[0], link.invite_link, reply_markup=markup)
            except:
                self.bot.send_message(ADMIN_IP_MISHA, f"Error send message to {user[0]}")

    def create_account(self, message):
        try:
            print(f"create_account {message.from_user.id}")
            self.data_base.add_user(message.from_user.id , message.from_user.username)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton("Set time zone")
            markup.add(item1)
            self.bot.send_message(message.from_user.id, NEED_TIME_ZONE_TEXT, reply_markup=markup)
            self.data_base_statistic.insert_new_user(message.from_user.id, message.from_user.username)
        except Exception("Create_Account Wrong") as e:
            self.bot.send_message(message.from_user.id, e)

    def set_time_zone(self, message):
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            for i in range(1, 8):
                item = types.KeyboardButton(f"Set time zone -{i} UTC")
                markup.add(item)
            markup.add(types.KeyboardButton(f"Set time zone +0 UTC"))
            for i in range(1, 8):
                item = types.KeyboardButton(f"Set time zone +{i} UTC")
                markup.add(item)
            self.bot.send_message(message.from_user.id, CHOOSE_TIME_ZONE_TEXT, reply_markup=markup)
        except Exception("Set_time_zone Wrong") as e:
            self.bot.send_message(message.from_user.id, e)

    def menu(self, message):
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton("Info")
            item2 = types.KeyboardButton("Set time zone")
            item3 = types.KeyboardButton("Set active time")
            item4 = types.KeyboardButton("Delete account")
            item5 = types.KeyboardButton("Stop searching")
            markup.add(item1, item2, item3, item4, item5)
            # self.bot.send_message(message.from_user.id, "-", reply_markup=markup)
            return markup
        except :
            self.bot.send_message(message.from_user.id, "menu Wrong")

    def have_not_account(self):
        markap = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markap.add(types.KeyboardButton("Info"))
        markap.add(types.KeyboardButton("Create account"))
        return markap
        
    def delete_account(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        try:
            print(f"delete_account {message.from_user.id}")
            item1 = types.KeyboardButton("Sure delete me")
            item2 = types.KeyboardButton("Menu")
            markup.add(item1, item2)
            self.bot.send_message(message.from_user.id, DELETE_ACCOUNT_TEXT, reply_markup=markup)
        except Exception("delete_account Wrong") as e:
            self.bot.send_message(message.from_user.id, e)
            

    def sure(self, message):
        try:
            user_id = message.from_user.id
            print(f"sure {user_id}")
            id_chat = self.data_base.loock_user_into_chats(user_id)
            self.data_base.delete_user(user_id)
            if id_chat:
                self.kick_members(id_chat[0][1], user_id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton("Create account")
            markup.add(item1)
            self.bot.send_message(user_id, DELETED_ACCOUNT_TEXT, reply_markup=markup)
        except Exception as e:
            self.bot.send_message(user_id, e)

    def stop_searching(self, message):
        try:
            print(f"stop_searching {message.from_user.id}")
            checker = self.data_base.get_user_info_from_id(message.from_user.id)
            if checker[7] == "False":
                self.bot.send_message(message.from_user.id, ALREADY_STOP_SEARCHING_TEXT)
                return
            self.data_base.change_active_status(message.from_user.id, "False")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(types.KeyboardButton("Menu"))
            self.bot.send_message(message.from_user.id, STOP_SEARCHING_TEXT, reply_markup=markup)
        except Exception("stop_searching Wrong") as e:
            self.bot.send_message(message.from_user.id, e)

    def set_time_zone_func(self, message, match):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        time_zone = match.group(1)     
        self.data_base.set_time_zone(message.from_user.id, time_zone)
        markup = self.menu(message)
        self.bot.send_message(message.from_user.id, f"Done, your time zone: {time_zone} hour/s ", reply_markup=markup)

    def set_active_time_panel(self, call):
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("See time options", callback_data="show_time_panel")
        markup.add(item1)
        self.start_message_id[call.from_user.id] = self.bot.send_message(call.chat.id, INSTRUCTION_FOR_SET_ACTIVE_TIME, reply_markup=markup).message_id
        
    def show_time_panel(self, call):
        markup = types.InlineKeyboardMarkup()
        column_1 = []
        column_2 = []
        for i in range(24):
            time = dt.time(hour=i, minute=0).strftime("%H:%M")
            column_1.append(types.InlineKeyboardButton(f"{time}", callback_data=f"starttime_{time}"))
            column_2.append(types.InlineKeyboardButton(f"{time}", callback_data=f"endtime_{time}"))
        for i in range(0, len(column_1)):
            markup.row(column_1[i], column_2[i])
        markup.add(types.InlineKeyboardButton("Hide", callback_data="Hide"))
        markup.add(types.InlineKeyboardButton("Start", callback_data="startsearching"))
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.start_message_id[call.from_user.id], text=f"{INSTRUCTION_FOR_SET_ACTIVE_TIME}\n\nStart time     -     End time", reply_markup=markup)

    def hide(self, call):
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Got it!", callback_data="show_time_panel")
        markup.add(item1)
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.start_message_id[call.from_user.id], text=INSTRUCTION_FOR_SET_ACTIVE_TIME, reply_markup=markup)
        


    def get_users_time(self, user_UTC_time, time_str):
        time_obj = dt.datetime.strptime(time_str, '%H:%M').time()
        time_delta = dt.timedelta(hours=abs(user_UTC_time))
        new_time_obj = (dt.datetime.combine(dt.date.today(), time_obj) + time_delta * (-1 if user_UTC_time > 0 else 1)).time()
        now = dt.datetime.now()
        today = now.replace(hour=new_time_obj.hour, minute=new_time_obj.minute, second=new_time_obj.second, microsecond=0)
        if today.time() < time_obj:
            today += dt.timedelta(days=1)
        return today.strftime("%Y-%m-%d %H:%M")












    def start_time(self, call, time):
        markup = self.menu(call)
        user_UTC_time = int(self.data_base.get_user_info_from_id(call.from_user.id)[3])
        new_time_obj = self.get_users_time(user_UTC_time ,time)
        
        self.bot.send_message(call.from_user.id, f"Your start time: {time}", reply_markup=markup)
        self.data_base.set_active_time_start(call.from_user.id, new_time_obj)

    def end_time(self, call, time):
        markup = self.menu(call)
        user_UTC_time = int(self.data_base.get_user_info_from_id(call.from_user.id)[3])
        new_time_obj = self.get_users_time(user_UTC_time ,time)
        
        self.bot.send_message(call.from_user.id, f"Your end time: {time}", reply_markup=markup)
        self.data_base.set_active_time_end(call.from_user.id, new_time_obj)
        
        
        

    def start_search(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(types.KeyboardButton("Menu"))
        person_info = self.data_base.get_user_info_from_id(message.from_user.id)
        self.data_base_statistic.user_push_start(message.from_user.id, message.from_user.username)
        if person_info[5] == None or person_info[6] == None:
            self.set_active_time_text(message, markup)
            return
        
        time_start_person = dt.datetime.strptime(person_info[5], '%Y-%m-%d %H:%M')
        time_end_person = dt.datetime.strptime(person_info[6], '%Y-%m-%d %H:%M')
        if time_start_person >= time_end_person:
            self.bot.send_message(message.from_user.id, INCORRECT__TIME_TEXT, reply_markup=markup)
            return
        if self.data_base.loock_user_into_chats(message.from_user.id):
            self.already_in_group(message, markup=markup)
            return
        self.bot.send_message(message.from_user.id, START_ACTIVE_TIME_TEXT, reply_markup=markup)
        self.data_base.change_active_status(message.from_user.id, "True")
        time.sleep(1)
        if len(self.data_base.get_match(time_start_person.strftime('%Y-%m-%d %H:%M'), time_end_person.strftime('%Y-%m-%d %H:%M'))) > 1:
            active_users = self.data_base.get_active_users(time_start_person.strftime('%Y-%m-%d %H:%M'), time_end_person.strftime('%Y-%m-%d %H:%M'))
            chat_id, name_room, _, _ = self.data_base.get_free_room_id(time_start_person.strftime('%Y-%m-%d %H:%M'), time_end_person.strftime('%Y-%m-%d %H:%M'))
            if chat_id == None:
                self.bot.send_message(message.from_user.id, "No free rooms")
                return
            pin = self.bot.get_chat(chat_id).pinned_message
            if pin is None:
                self.pin_first_message(chat_id)
            link = self.bot.create_chat_invite_link(chat_id = chat_id, name=name_room, expire_date= dt.datetime.now()+dt.timedelta(minutes=30))
            self.send_links_to_users(active_users, link, markup)
        else:
            self.bot.send_message(message.from_user.id, DONT_FOUND_MATCH_TEXT, reply_markup=markup)
        
    #Send data base 
    def get_bd(self, message, db_name:str, table_name:str=None, columns:list=None):
        try:
            if table_name != None:
                self.exel_creator.get_statistic_exel(table_name, columns)
                db_name = table_name + ".xlsx"
            with open(db_name, 'rb') as file:
                self.bot.send_document(message.from_user.id, file)
        except Exception as e:
            print(e)
            
    def join_request(self, update: types.ChatJoinRequest):
        self.bot.delete_message(chat_id=update.chat.id, message_id=update.message_id)
        user_id = update.from_user.id
        chat_id = update.chat.id
        self.data_base_statistic.user_came(update.from_user.id, update.from_user.username, update.chat.id)
        self.data_base.change_active_status(user_id, "False")
        self.data_base.add_user_to_Active_Chat(user_id, chat_id)
        self.upgrade_room_info_time(chat_id)
        count = self.bot.get_chat_member_count(chat_id) - 1
        self.data_base.update_rooms_users_count(chat_id, count)
        self.bot.send_message(user_id, JOIN_GROUP_TEXT)
    
    def left_chat_member(self, message):
            user_id = message.from_user.id
            chat_id = message.chat.id
            self.data_base.dell_user_from_Active_Chat(user_id)
            self.data_base.change_active_status(user_id, "False")
            self.upgrade_room_info_time(chat_id)
            if time.localtime().tm_min != 0:
                self.bot.send_message(user_id, REMOVED_FROM_GROUP_TEXT)
            count = self.bot.get_chat_member_count(chat_id) - 1
            self.data_base.update_rooms_users_count(chat_id, count)
            if count == 0:
                messages = self.data_base.get_messages_from_chat(chat_id)
                for i in messages:
                    try: 
                        self.bot.delete_message(i[0], i[1])
                    except:
                        self.bot.send_message(ADMIN_IP_MISHA, f"Error delete_message: {i[0]}, {i[1]}")
                self.data_base.delete_chat_messages_from_user(user_id)
            self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            
    def add_chat_into_active(self, message):
            try:
                chat_id = message.chat.id
                if int(message.from_user.id) in TOTAL_ADMINS:
                    self.data_base.add_chat_into_active(chat_id, message.chat.title)
                    self.bot.send_message(chat_id, f"Chat added chat_id: {chat_id}")
                else:
                    self.bot.send_message(chat_id, "You can't do it")
            except Exception("add_chat_into_active Wrong") as e:
                self.bot.send_message(chat_id, e)
                
    def delete_chat_from_active(self, message):
        try:
            chat_id = message.chat.id
            if int(message.from_user.id) in  TOTAL_ADMINS:
                self.data_base.delete_chat_from_active(chat_id)
                self.bot.send_message(chat_id, "Chat deleted")
            else:
                self.bot.send_message(chat_id, "You can't do it")
        except Exception("delete_chat_from_active Wrong") as e:
            self.bot.send_message(chat_id, e)
            
    def send_start(self, message):
        try:
            markup = types.ReplyKeyboardMarkup(row_width=2)
            markup.add(types.KeyboardButton("Info"))
            cheker = self.data_base.get_one_user(message.from_user.id)
            if cheker == 1:
                item1 = types.KeyboardButton("Menu")
                message_txt = "Welcome back"
            else:
                item1 = types.KeyboardButton("Create account")
                message_txt = "Welcome!"
            markup.add(item1)
            self.bot.send_message(message.from_user.id, message_txt, reply_markup=markup)
        except Exception("Start Wrong") as e:
            self.bot.send_message(message.from_user.id, e)
            
    def handle_callback_query(self, call):
        if self.data_base.get_one_user(call.from_user.id) != None:
            start_func = call.data.split("_")
            if start_func[0] == "starttime":
                self.start_time(call, start_func[1])
            elif start_func[0] == 'endtime':
                self.end_time(call, start_func[1])
            elif start_func[0] == "startsearching":
                self.start_search(call)
            elif "_".join(start_func) == "show_time_panel":
                self.show_time_panel(call)
            elif start_func[0] == 'Hide':
                self.hide(call)
        else:
            markup = self.have_not_account()
            self.bot.send_message(call.from_user.id, HAVE_NO_ACCOUNT_TEXT, reply_markup=markup)
            
    def get_log(self, message):
        try:
            data = os.path.join(os.getcwd(), "error_logs", "logs.txt")
            with open(data, 'rb') as file:
                self.bot.send_document(message.from_user.id, file)
        except Exception as e:
            print(e)
        
    def text_holder(self, message):
        self.data_base.write_messag_history(message.chat.id, message.from_user.id, message.id)
        if message.text == "Dell all" and message.from_user.id == ADMIN_IP_MISHA:
            self.dell_all()
            return
        elif message.text == "Version":
            self.bot.send_message(message.chat.id, VERSION)
            return

        if message.text not in ["Info", "Create account", "Set time zone"] and self.data_base.get_one_user(message.from_user.id) is None:
            markup = self.have_not_account()
            self.bot.send_message(message.from_user.id, HAVE_NO_ACCOUNT_TEXT, reply_markup=markup)
        elif self.get_match(message):
            self.set_time_zone_func(message, self.get_match(message))
            self.bot.send_message(ADMIN_IP_MISHA, f"User {message.from_user.first_name} set time zone {self.get_match(message)}")
        elif message.text == "Menu":
            markup = self.menu(message)
            self.bot.send_message(message.from_user.id, CHOOSE_MOUTION_TEXT, reply_markup=markup)
        elif message.text == "Set time zone":
            self.set_time_zone(message) 
        elif message.text == "Set active time":
            self.set_active_time_panel(message)
        elif message.text == "Delete account":
            self.delete_account(message)
        elif message.text == "Info":
            markup = self.menu(message)
            self.bot.send_message(message.from_user.id, INFO_TEXT, reply_markup=markup)
        elif message.text == "Sure delete me":
            self.sure(message)
        elif message.text == "Create account":
            self.create_account(message)
        elif message.text == "Stop searching":
            self.stop_searching(message)
        elif message.text == "GET GROUPS":
            groups = self.data_base.get_all_groups()
            for i in groups:
                link = self.bot.create_chat_invite_link(chat_id=i[1], name=i[2])
                self.bot.send_message(message.from_user.id, link)
        elif message.text == "GET STAT 2":
            self.get_bd(message, 'Statistic.db', "user_activity_start", ["id", "user_id", "user_name", "came_time"])
            self.get_bd(message, 'Statistic.db', "user_came", ["id", "user_id", "user_name", "chat_id", "came_time"])
        elif message.text == "GET STAT 1":
            self.get_bd(message, 'Statistic.db', "users", ["id", "user_id", "user_name"])
        elif message.text == "GET DB":
            self.get_bd(message,'AsyaApp.db') 
            self.get_bd(message, 'Statistic.db')
        elif message.text == "er":
            self.er_func()
        elif message.text == "get_log":
            self.get_log(message)
    
    @Decoration().decore_bd_function
    def er_func(self):
        100 / 0
    
    def start(self):
        @self.bot.message_handler(content_types=['new_chat_members'])
        def join_request_handler(update: types.ChatJoinRequest):
            self.check_event()
            self.join_request(update)
            self.bot.send_message(ADMIN_IP_MISHA, f"{update.from_user.first_name} join chat {update.chat.id}")

        # If users leave chat
        @self.bot.message_handler(content_types=['left_chat_member'])
        def left_chat_member_handler(update: types.ChatMemberLeft):
            self.check_event()
            print("left_chat_member_handler")
            self.left_chat_member(update)
            self.bot.send_message(ADMIN_IP_MISHA, f"{update.from_user.first_name} left chat {update.chat.id}")

        # If create new chat
        @self.bot.message_handler(commands=['add_chat_into_active'])
        def add_chat_into_active_handler(update: types.ChatJoinRequest):
            self.check_event()
            self.add_chat_into_active(update)

        #  If delete chat
        @self.bot.message_handler(commands=['delete_chat_from_active'])
        def delete_chat_from_active_handler(update: types.ChatJoinRequest):
            self.check_event()
            self.delete_chat_from_active(update)

        @self.bot.message_handler(commands=['start'])
        def send_start_hanlder(update: types.ChatJoinRequest):
            self.check_event()
            self.send_start(update)
            self.bot.send_message(ADMIN_IP_MISHA, f"{update.from_user.first_name} start bot")

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback_query_handler(call: types.CallbackQuery):
            self.check_event()
            self.handle_callback_query(call)
            self.bot.send_message(ADMIN_IP_MISHA, f"{call.from_user.first_name} click {call.data}")

        @self.bot.message_handler(content_types='text')
        def text_holder_hanlder(call: types.CallbackQuery):
            self.check_event()
            self.text_holder(call)
        self.bot.polling(none_stop=True)


        
if __name__ == '__main__':
    # while True:
        # try:
        time.sleep(1)
        event = threading.Event()
        bot = CreativeHour(API, event)
        time_cheker = TimeCheker(event, bot=bot)
        t = threading.Thread(target=time_cheker.time_cheker)
        t.daemon = True 
        t.start()
        bot.start()
        # except Exception as e:
        #     print(f"Dangerous_Error: {e}")
