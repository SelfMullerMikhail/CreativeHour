import telebot
from telebot import types
from bd_function import BdHelper
import threading
import re
import datetime as dt
from loger import write_logs
from CONSTAINS import *
import time


class CreativeHour():
    def __init__(self, *args):
        super().__init__()
        self.args = args
        self.API = API
        self.data_base = BdHelper('AsyaApp.db')
        self.data_base_statistic = BdHelper('Statistic.db')
        self.start_message_id = {}
    
    def start(self):
        bot = telebot.TeleBot(*self.args)
        def upgrade_room_info_time(id_chat):
            min_time, max_time = self.data_base.get_time_active_chat_users(id_chat)
            self.data_base.update_room_info_time(id_chat, min_time, 'min_start_time')
            self.data_base.update_room_info_time(id_chat, max_time, 'max_end_time')
            return None

        def dell_all():
                users = self.data_base.get_all_users()
                chats = self.data_base.get_all_chats()
                for chat in chats:
                    for user in users:
                        kick_members(chat[0], user[0])
                self.data_base.dell_all_ReadyUsers()
                self.data_base.dell_all_Active_Chat()
                self.data_base.dell_all_Messages()

        def get_match(message):
            return re.search(r'Set time zone ([-+]\d) UTC', message.text)   

        def get_UTC_form_time(time):
            time_person = dt.datetime.strptime(time, '%H:%M').time()
            return time_person.strftime('%H:%M') 

        def already_in_group(message, markup):
            bot.send_message(ADMIN_IP_MISHA, f"{message.from_user.id} already in group")
            bot.send_message(message.from_user.id, ALREADY_IN_GROUP_TEXT, reply_markup=markup)

        def set_active_time_text(message, markup):
                bot.send_message(message.from_user.id, SET_ACTIVE_TIME_TEXT, reply_markup=markup)

        def pin_first_message(chat_id):
                first_message = bot.send_message(chat_id=chat_id, text=FIRST_MESSAGE_GROUP)
                bot.pin_chat_message(chat_id=chat_id, message_id=first_message.message_id)

        def send_links_to_users(active_users, link, markup):
            for user in active_users:
                try:
                    bot.send_message(ADMIN_IP_MISHA, f"Send link to {user[2]}")
                    bot.send_message(user[0], link.invite_link, reply_markup=markup)
                except:
                    bot.send_message(ADMIN_IP_MISHA, f"Error send message to {user[0]}")

        def create_account(message):
            try:
                print(f"create_account {message.from_user.id}")
                self.data_base.add_user(message.from_user.id , message.from_user.username)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                item1 = types.KeyboardButton("Set time zone")
                markup.add(item1)
                bot.send_message(message.from_user.id, NEED_TIME_ZONE_TEXT, reply_markup=markup)
                self.data_base_statistic.insert_new_user(message.from_user.id, message.from_user.username)
            except Exception("Create_Account Wrong") as e:
                bot.send_message(message.from_user.id, e)

        def set_time_zone(message):
            try:
                print(f"set_time_zone {message.from_user.id}")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                for i in range(1, 8):
                    item = types.KeyboardButton(f"Set time zone -{i} UTC")
                    markup.add(item)
                markup.add(types.KeyboardButton(f"Set time zone +0 UTC"))
                for i in range(1, 8):
                    item = types.KeyboardButton(f"Set time zone +{i} UTC")
                    markup.add(item)
                bot.send_message(message.from_user.id, CHOOSE_TIME_ZONE_TEXT, reply_markup=markup)
            except Exception("Set_time_zone Wrong") as e:
                bot.send_message(message.from_user.id, e)

        def menu(message):
            try:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                item1 = types.KeyboardButton("Info")
                item2 = types.KeyboardButton("Set time zone")
                item3 = types.KeyboardButton("Set active time")
                item4 = types.KeyboardButton("Delete account")
                item5 = types.KeyboardButton("Stop searching")
                markup.add(item1, item2, item3, item4, item5)
                # bot.send_message(message.from_user.id, "-", reply_markup=markup)
                return markup
            except :
                bot.send_message(message.from_user.id, "menu Wrong")

        def have_not_account():
            markap = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markap.add(types.KeyboardButton("Info"))
            markap.add(types.KeyboardButton("Create account"))
            return markap
            
        def send_message(self, user_id, text):
            try:
                bot.send_message(user_id, text)
            except:
                pass
            
        def delete_account(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            try:
                print(f"delete_account {message.from_user.id}")
                item1 = types.KeyboardButton("Sure delete me")
                item2 = types.KeyboardButton("Menu")
                markup.add(item1, item2)
                bot.send_message(message.from_user.id, DELETE_ACCOUNT_TEXT, reply_markup=markup)
            except Exception("delete_account Wrong") as e:
                bot.send_message(message.from_user.id, e)
                
        def kick_members(chat_id:int, user_id:int):
            try:
                bot.kick_chat_member(chat_id=chat_id, user_id= user_id)
                bot.unban_chat_member(chat_id=chat_id, user_id= user_id)
            except Exception as e:
                print(e)

        def sure(message):
            try:
                user_id = message.from_user.id
                print(f"sure {user_id}")
                id_chat = self.data_base.loock_user_into_chats(user_id)
                self.data_base.delete_user(user_id)
                if id_chat:
                    kick_members(id_chat[0][1], user_id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                item1 = types.KeyboardButton("Create account")
                markup.add(item1)
                bot.send_message(user_id, DELETED_ACCOUNT_TEXT, reply_markup=markup)
            except Exception as e:
                bot.send_message(user_id, e)

        def stop_searching(message):
            try:
                print(f"stop_searching {message.from_user.id}")
                checker = self.data_base.get_user_info_from_id(message.from_user.id)
                if checker[7] == "False":
                    bot.send_message(message.from_user.id, ALREADY_STOP_SEARCHING_TEXT)
                    return
                self.data_base.change_active_status(message.from_user.id, "False")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(types.KeyboardButton("Menu"))
                bot.send_message(message.from_user.id, STOP_SEARCHING_TEXT, reply_markup=markup)
            except Exception("stop_searching Wrong") as e:
                bot.send_message(message.from_user.id, e)

        def set_time_zone_func(message, match):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            time_zone = match.group(1)     
            self.data_base.set_time_zone(message.from_user.id, time_zone)
            markup = menu(message)
            bot.send_message(message.from_user.id, f"Done, your time zone: {time_zone} hour/s ", reply_markup=markup)
            bot.send_message(ADMIN_IP_MISHA, f"User {message.from_user.id} set time zone {time_zone}")

        def set_active_time_panel(call):
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Got it!", callback_data="show_time_panel")
            markup.add(item1)
            self.start_message_id[call.from_user.id] = bot.send_message(call.chat.id, INSTRUCTION_FOR_SET_ACTIVE_TIME, reply_markup=markup).message_id
            
        def show_time_panel(call):
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
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.start_message_id[call.from_user.id], text=f"{INSTRUCTION_FOR_SET_ACTIVE_TIME}\n\nStart time     -     End time", reply_markup=markup)

        def hide(call):
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Got it!", callback_data="show_time_panel")
            markup.add(item1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.start_message_id[call.from_user.id], text=INSTRUCTION_FOR_SET_ACTIVE_TIME, reply_markup=markup)
            

        def get_users_time(user_id, time_str):
            user_UTC_time = int(self.data_base.get_user_info_from_id(user_id)[3])
            time_obj = dt.datetime.strptime(time_str, '%H:%M').time()
            time_delta = dt.timedelta(hours=abs(user_UTC_time))
            if user_UTC_time <= 0:
                new_time_obj = (dt.datetime.combine(dt.date.today(), time_obj) + time_delta).time()
            else:
                new_time_obj = (dt.datetime.combine(dt.date.today(), time_obj) - time_delta).time()
            formatted_time_str = new_time_obj.strftime('%H:%M')
            return formatted_time_str

        def start_time(call, time):
            markup = menu(call)
            new_time_obj = get_users_time(call.from_user.id ,time)
            bot.send_message(call.from_user.id, f"Your start time: {time}", reply_markup=markup)
            self.data_base.set_active_time_start(call.from_user.id, new_time_obj)
            bot.send_message(ADMIN_IP_MISHA, f"{call.from_user.id} set start time {time} UTC")

        def end_time(call, time):
            markup = menu(call)
            new_time_obj = get_users_time(call.from_user.id ,time)
            bot.send_message(call.from_user.id, f"Your end time: {time}", reply_markup=markup)
            self.data_base.set_active_time_end(call.from_user.id, new_time_obj)
            bot.send_message(ADMIN_IP_MISHA, f"{call.from_user.id} set end time {time} UTC")

        def start_search(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(types.KeyboardButton("Menu"))
            person_info = self.data_base.get_user_info_from_id(message.from_user.id)
            self.data_base_statistic.user_push_start(message.from_user.id, message.from_user.username)
            if person_info[5] == None or person_info[6] == None:
                set_active_time_text(message, markup)
                return
            time_start_person = get_UTC_form_time(person_info[5])
            time_end_person = get_UTC_form_time(person_info[6])
            if time_start_person >= time_end_person:
                bot.send_message(message.from_user.id, INCORRECT__TIME_TEXT, reply_markup=markup)
                return
            if self.data_base.loock_user_into_chats(message.from_user.id):
                already_in_group(message, markup=markup)
                return
            bot.send_message(message.from_user.id, START_ACTIVE_TIME_TEXT, reply_markup=markup)
            self.data_base.change_active_status(message.from_user.id, "True")
            time.sleep(1)
            if len(self.data_base.get_match(time_start_person, time_end_person)) > 1:
                active_users = self.data_base.get_active_users(time_start_person, time_end_person)
                chat_id, name_room, _, _ = self.data_base.get_free_room_id(time_start_person, time_end_person)
                if chat_id == None:
                    bot.send_message(message.from_user.id, "No free rooms")
                    return
                pin = bot.get_chat(chat_id).pinned_message
                if pin is None:
                    pin_first_message(chat_id)
                link = bot.create_chat_invite_link(chat_id = chat_id, name=name_room, expire_date= dt.datetime.now()+dt.timedelta(minutes=30))
                send_links_to_users(active_users, link, markup)
            else:
                bot.send_message(message.from_user.id, DONT_FOUND_MATCH_TEXT, reply_markup=markup)
            
        #Send data base 
        def get_bd(bd):
            try:
                with open(bd, 'rb') as file:
                    bot.send_document(ADMIN_IP_MISHA, file)
            except Exception as e:
                print(e)
                

        @bot.message_handler(content_types=['new_chat_members'])
        def join_request(update: types.ChatJoinRequest):
            bot.delete_message(chat_id=update.chat.id, message_id=update.message_id)
            user_id = update.from_user.id
            chat_id = update.chat.id
            self.data_base_statistic.user_came(update.from_user.id, update.from_user.username, update.chat.id)
            self.data_base.change_active_status(user_id, "False")
            self.data_base.add_user_to_Active_Chat(user_id, chat_id)

            upgrade_room_info_time(chat_id)

            count = bot.get_chat_member_count(chat_id) - 1
            print("Count: ",count)
            self.data_base.update_rooms_users_count(chat_id, count)
            bot.send_message(user_id, JOIN_GROUP_TEXT)
            bot.send_message(ADMIN_IP_MISHA, f"New user: {user_id}")
            
            # @bot.message_handler(content_types=['service'])
            # def handle_service_message(message):
            #     bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        # If users leave chat
        @bot.message_handler(content_types=['left_chat_member'])
        def left_chat_member(message):
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            user_id = message.from_user.id
            chat_id = message.chat.id
            self.data_base.dell_user_from_Active_Chat(user_id)
            self.data_base.change_active_status(user_id, "False")
            upgrade_room_info_time(chat_id)
            if time.localtime().tm_min != 0:
                bot.send_message(user_id, REMOVED_FROM_GROUP_TEXT)
            count = bot.get_chat_member_count(chat_id) - 1
            self.data_base.update_rooms_users_count(chat_id, count)
            print("Count: ",count)
            if count == 0:
                # self.data_base.set_chats_time(chat_id, "None", "None")
                messages = self.data_base.get_messages_from_chat(chat_id)
                for i in messages:
                    try: 
                        bot.delete_message(i[0], i[1])
                    except:
                        bot.send_message(ADMIN_IP_MISHA, f"Error delete_message: {i[0]}, {i[1]}")
                self.data_base.delete_chat_messages_from_user(user_id)

        # If create new chat
        @bot.message_handler(commands=['add_chat_into_active'])
        def add_chat_into_active(message):
            try:
                print(f"add_chat_into_active {message.chat.id}")
                chat_id = message.chat.id
                if int(message.from_user.id) in TOTAL_ADMINS:
                    self.data_base.add_chat_into_active(chat_id, message.chat.title)
                    bot.send_message(chat_id, f"Chat added chat_id: {chat_id}")
                else:
                    bot.send_message(chat_id, "You can't do it")
            except Exception("add_chat_into_active Wrong") as e:
                bot.send_message(chat_id, e)

        #  If delete chat
        @bot.message_handler(commands=['delete_chat_from_active'])
        def delete_chat_from_active(message):
            try:
                print(f"delete_chat_from_active {message.chat.id}")
                chat_id = message.chat.id
                if int(message.from_user.id) in  TOTAL_ADMINS:
                    self.data_base.delete_chat_from_active(chat_id)
                    bot.send_message(chat_id, "Chat deleted")
                else:
                    bot.send_message(chat_id, "You can't do it")
            except Exception("delete_chat_from_active Wrong") as e:
                bot.send_message(chat_id, e)

        @bot.message_handler(commands=['start'])
        def send_start(message):
            try:
                print(f"start {message.from_user.id}")
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
                bot.send_message(message.from_user.id, message_txt, reply_markup=markup)
            except Exception("Start Wrong") as e:
                bot.send_message(message.from_user.id, e)

        @bot.callback_query_handler(func=lambda call: True)
        def handle_callback_query(call):
            if self.data_base.get_one_user(call.from_user.id) != None:
                start_func = call.data.split("_")
                if start_func[0] == "starttime":
                    th_start_time = threading.Thread(target=start_time, args=(call, start_func[1]))
                    th_start_time.start()
                elif start_func[0] == 'endtime':
                    th_end_time = threading.Thread(target=end_time, args=(call, start_func[1]))
                    th_end_time.start()
                elif start_func[0] == "startsearching":
                    th_start_search = threading.Thread(target=start_search, args=(call,))
                    th_start_search.start()
                elif "_".join(start_func) == "show_time_panel":
                    print("show_time_panel")
                    show_time_panel(call)
                elif start_func[0] == 'Hide':
                    hide(call)
            else:
                markup = have_not_account()
                bot.send_message(call.from_user.id, HAVE_NO_ACCOUNT_TEXT, reply_markup=markup)

        @bot.message_handler(content_types='text')
        def text_holder(message):
            self.data_base.write_messag_history(message.chat.id, message.from_user.id, message.id)
            if message.text == "Dell all" and message.from_user.id == ADMIN_IP_MISHA:
                dell_all()
                return
            elif message.text == "Version":
                bot.send_message(message.chat.id, VERSION)
                return

            if message.text not in ["Info", "Create account", "Set time zone"] and self.data_base.get_one_user(message.from_user.id) is None:
                markup = have_not_account()
                bot.send_message(message.from_user.id, HAVE_NO_ACCOUNT_TEXT, reply_markup=markup)
            elif get_match(message):
                set_time_zone_func(message, get_match(message))
            elif message.text == "Menu":
                markup = menu(message)
                bot.send_message(message.from_user.id, CHOOSE_MOUTION_TEXT, reply_markup=markup)
            elif message.text == "Set time zone":
                set_time_zone(message) 
            elif message.text == "Set active time":
                set_active_time_panel(message)
            elif message.text == "Delete account":
                delete_account(message)
            elif message.text == "Info":
                markup = menu(message)
                bot.send_message(message.from_user.id, INFO_TEXT, reply_markup=markup)
            elif message.text == "Sure delete me":
                sure(message)
            elif message.text == "Create account":
                create_account(message)
            elif message.text == "Stop searching":
                stop_searching(message)
            elif message.text == "GET GROUPS":
                groups = self.data_base.get_all_groups()
                for i in groups:
                    link = bot.create_chat_invite_link(chat_id=i[1], name=i[2])
                    bot.send_message(message.from_user.id, link)
            elif message.text == "GET DB S":
                get_bd('Statistic.db')
            elif message.text == "GET DB U": 
                get_bd('AsyaApp.db')
        bot.polling(none_stop=True)

        


from time_cheker_threading import TimeCheker
if __name__ == '__main__':
    while True:
        try:
            bot = CreativeHour(API)
            time_cheker = TimeCheker(bot=bot)
            t = threading.Thread(target=time_cheker.time_cheker)
            t.daemon = True 
            t.start()
            bot.start()
        except Exception as e:
            print(f"Dangerous_Error: {e}")
            bot.send_message(ADMIN_IP_MISHA, f"Dangerous_Error: {e}")
