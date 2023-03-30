import telebot
from telebot import types
from bd_function import BdHelper
import threading
import re
import datetime as dt
from loger import write_logs
from CONSTAINS import *
import time




bot = telebot.TeleBot(API)
data_base = BdHelper()

@bot.message_handler(content_types=['new_chat_members'])
def join_request(update: types.ChatJoinRequest):
    user_id = update.from_user.id
    chat_id = update.chat.id
    info = data_base.get_user_info_from_id(user_id)
    data_base.change_active_status(user_id, "False")
    data_base.add_user_to_Active_Chat(user_id, chat_id)
    data_base.upgrade_room_info_append(user_id, info[5], info[6])
    count = bot.get_chat_member_count(chat_id) - 1
    data_base.update_rooms_users_count(chat_id, count)

# If users leave chat
@bot.message_handler(content_types=['left_chat_member'])
def left_chat_member(message=None, user_id_=None, chat_id_=None):
    if message is None:
        user_id = user_id_
        chat_id = chat_id_
    else:
        user_id = message.from_user.id
        chat_id = message.chat.id
    data_base.dell_user_from_Active_Chat(chat_id, user_id)
    data_base.change_active_status(user_id, "False")
    time_min, time_max = data_base.get_time_from_chat(chat_id)
    data_base.upgrade_room_info_delete(chat_id, time_min, time_max)
    bot.send_message(user_id, REMOVED_FROM_GROUP_TEXT)
    count = bot.get_chat_member_count(chat_id) 
    count = count - 1
    data_base.update_rooms_users_count(chat_id, count)
    
    if count <= 1:
        data_base.set_chats_time(chat_id, "NULL", "NULL")
        messages = data_base.get_messages_from_chat(chat_id)
        for i in messages:
            try:
                bot.delete_message(i[0], i[1])
            except:
                bot.send_message(ADMIN_IP_MISHA, f"Error delete_message: {i[0]}, {i[1]}")
        data_base.delete_chat_messages_from_user(user_id)

# If create new chat
@bot.message_handler(commands=['add_chat_into_active'])
def add_chat_into_active(message):
    try:
        print(f"add_chat_into_active {message.chat.id}")
        chat_id = message.chat.id
        if int(message.from_user.id) in TOTAL_ADMINS:
            data_base.add_chat_into_active(chat_id, message.chat.title)
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
            data_base.delete_chat_from_active(chat_id)
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
        cheker = data_base.get_one_user(message.from_user.id)
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

def create_account(message):
    try:
        print(f"create_account {message.from_user.id}")
        data_base.add_user(message.from_user.id , message.from_user.username)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Set time zone")
        markup.add(item1)
        bot.send_message(message.from_user.id, NEED_TIME_ZONE_TEXT, reply_markup=markup)
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

def sure(message):
    try:
        print(f"sure {message.from_user.id}")
        id_chat = data_base.loock_user_into_chats(message.from_user.id)
        # count = bot.get_chat_members_count(id_chat) - 1
        # data_base.update_rooms_users_count(id_chat, count)
        # left_chat_member(user_id_=message.from_user.id, chat_id=id_chat)
        data_base.delete_user(message.from_user.id)
        if id_chat:
            bot.kick_chat_member(chat_id=id_chat, user_id= message.from_user.id)
            bot.unban_chat_member(chat_id=id_chat, user_id= message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Create account")
        markup.add(item1)
        bot.send_message(message.from_user.id, DELETED_ACCOUNT_TEXT, reply_markup=markup)
    except Exception("Sure Wrong") as e:
        bot.send_message(message.from_user.id, e)

def stop_searching(message):
    try:
        print(f"stop_searching {message.from_user.id}")
        checker = data_base.get_user_info_from_id(message.from_user.id)
        if checker[7] == "False":
            bot.send_message(message.from_user.id, ALREADY_STOP_SEARCHING_TEXT)
            return
        data_base.change_active_status(message.from_user.id, "False")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Menu")
        markup.add(item1)
        bot.send_message(message.from_user.id, STOP_SEARCHING_TEXT, reply_markup=markup)
    except Exception("stop_searching Wrong") as e:
        bot.send_message(message.from_user.id, e)

def set_time_zone_func(message, match):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    time_zone = match.group(1)     
    data_base.set_time_zone(message.from_user.id, time_zone)
    markup = menu(message)
    bot.send_message(message.from_user.id, f"Done, your time zone: {time_zone} hour/s ", reply_markup=markup)


def set_active_time_panel(call):
    markup = types.InlineKeyboardMarkup()
    column_1 = []
    column_2 = []
    for i in range(24):
        time = dt.time(hour=i, minute=0).strftime("%H:%M")
        column_1.append(types.InlineKeyboardButton(f"{time}", callback_data=f"starttime_{time}"))
        column_2.append(types.InlineKeyboardButton(f"{time}", callback_data=f"endtime_{time}"))
    for i in range(0, len(column_1)):
        markup.row(column_1[i], column_2[i])
    markup.add(types.InlineKeyboardButton("Start", callback_data="startsearching"))
    bot.send_message(call.chat.id, INSTRUCTION_FOR_SET_ACTIVE_TIME, reply_markup=markup)

def get_UTC_time(user_id, time_str):
    user_UTC_time = int(data_base.get_user_info_from_id(user_id)[3])
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
    new_time_obj = get_UTC_time(call.from_user.id ,time)
    bot.send_message(call.from_user.id, f"Your start time: {time}", reply_markup=markup)
    data_base.set_active_time_start(call.from_user.id, new_time_obj)

def end_time(call, time):
    markup = menu(call)
    new_time_obj = get_UTC_time(call.from_user.id ,time)
    bot.send_message(call.from_user.id, f"Your end time: {time}", reply_markup=markup)
    data_base.set_active_time_end(call.from_user.id, new_time_obj)

def start_search(message):
    bot.send_message(ADMIN_IP_MISHA, f"{message.from_user.id} start searching")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("Menu"))
    data_base.change_active_status(message.from_user.id, "True")
    person_info = data_base.get_user_info_from_id(message.from_user.id)
    if person_info[5] == None or person_info[6] == None:
        bot.send_message(ADMIN_IP_MISHA, f"{message.from_user.id} set time None")
        bot.send_message(message.from_user.id, SET_ACTIVE_TIME_TEXT, reply_markup=markup)
        return
    time_start_person = dt.datetime.strptime(person_info[5], '%H:%M').time()
    time_start_person = time_start_person.strftime('%H:%M') 
    time_end_person = dt.datetime.strptime(person_info[6], '%H:%M').time() 
    time_end_person = time_end_person.strftime('%H:%M')
    if time_start_person >= time_end_person:
        bot.send_message(message.from_user.id, INCORRECT__TIME_TEXT, reply_markup=markup)
        return
    user_active = data_base.loock_user_into_chats(message.from_user.id)
    if user_active:
        bot.send_message(ADMIN_IP_MISHA, f"{message.from_user.id} already in group")
        bot.send_message(message.from_user.id, ALREADY_IN_GROUP_TEXT, reply_markup=markup)
        return
    bot.send_message(message.from_user.id, START_ACTIVE_TIME_TEXT, reply_markup=markup)
    data_base.change_active_status(message.from_user.id, "True")
    users = data_base.get_match(time_start_person, time_end_person)
    if len(users) > 1:
        active_users = data_base.get_active_users(time_start_person, time_end_person)
        chat_id, name_room = data_base.get_free_room_id(time_start_person, time_end_person)
        if chat_id == None:
            bot.send_message(message.from_user.id, "No free rooms")
            return
        link = bot.create_chat_invite_link(chat_id = chat_id, name=name_room, expire_date= dt.datetime.now()+dt.timedelta(minutes=30))
        for user in active_users:
            try:
                bot.send_message(ADMIN_IP_MISHA, f"Send link to {user[2]}")
                bot.send_message(user[0], f"{APPROVE_TO_JOIN_TEXT}  {user[2]}-{user[3]}", reply_markup=markup)
                bot.send_message(user[0], link.invite_link)
            except:
                bot.send_message(ADMIN_IP_MISHA, f"Error send message to {user[0]}")
    else:
        bot.send_message(ADMIN_IP_MISHA, DONT_FOUND_MATCH_TEXT, reply_markup=markup)
        bot.send_message(message.from_user.id, DONT_FOUND_MATCH_TEXT, reply_markup=markup)

def check_persons(message, markup):
    try:
        info = data_base.get_info_all_users_in_chats()
        html = ""
        for i in info:
            try:
                user = f"""name: {i[1]}  id: {i[0]}   time_zone: {i[2]} id_chat:{i[3]}   name_chat: {i[4]} 
    s_time: {i[5]}   e_time {i[6]} \n"""
                html = str(html) + str(user)
            except:
                pass
        try:
            bot.send_message(message.from_user.id, html, reply_markup=markup)
        except:
            pass
    except:
        pass



@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if data_base.get_one_user(call.from_user.id) != None:
        start_func = call.data.split("_")
        if start_func[0] == "starttime":
            start_time(call, start_func[1])
        elif start_func[0] == 'endtime':
            end_time(call, start_func[1])
        elif start_func[0] == "startsearching":
            start_search(call)
    else:
        markup = have_not_account()
        bot.send_message(call.from_user.id, HAVE_NO_ACCOUNT_TEXT, reply_markup=markup)

def have_not_account():
    markap = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markap.add(types.KeyboardButton("Info"))
    markap.add(types.KeyboardButton("Create account"))
    return markap

def dell_all():
        users = data_base.get_all_users()
        chats = data_base.get_all_chats()
        for chat in chats:
            for user in users:
                try:
                    bot.delete_message(chat[0], user[0])
                except:
                    pass
                try:
                    bot.kick_chat_member(chat[0], user[0])
                except:
                    pass
                try:
                    bot.unban_chat_member(chat[0], user[0])
                except:
                    pass
        data_base.dell_all_ReadyUsers()
        data_base.dell_all_Active_Chat()
        data_base.dell_all_Messages()

def dell_all_message_from_one_chat(info):
    messages = data_base.get_messages_from_chat(info.chat.id)
    for message in messages:
        try:
            bot.delete_message(info.chat.id, message[0])
        except:
            pass
    data_base.delete_chat_messages_from_user(info.chat.id)

def get_match(message):
    return re.search(r'Set time zone ([-+]\d) UTC', message.text)   


@bot.message_handler(content_types='text')
def text_holder(message):
    data_base.write_messag_history(message.chat.id, message.from_user.id, message.id)
    if message.text == "Dell all" and message.from_user.id == ADMIN_IP_MISHA:
        dell_all()
        return
    elif message.text == "Version":
        bot.send_message(message.chat.id, "Version 5.5")
        return
    elif message.text == "Dell all message" and message.from_user.id == ADMIN_IP_MISHA:
        dell_all_message_from_one_chat(message)
        return
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if message.text not in ["Info", "Create account"] and data_base.get_one_user(message.from_user.id) is None:
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
    elif message.text == "Check persons":
        if int(message.from_user.id) in TOTAL_ADMINS:
            check_persons(message, markup)
            return
        


from time_cheker_threading import TimeCheker
if __name__ == '__main__':
    while True:
        try:
            time_cheker = TimeCheker(database=data_base, bot=bot, write_logs=write_logs, left_chat_member=left_chat_member)
            t = threading.Thread(target=time_cheker.time_cheker)
            t.daemon = True 
            t.start()
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Dangerous_Error: {e}")
            bot.send_message(ADMIN_IP_MISHA, f"Dangerous_Error: {e}")
