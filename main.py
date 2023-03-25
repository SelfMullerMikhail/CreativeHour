import telebot
from telebot import types
from bd_function import BdHelper
import threading
import re
import datetime as dt
from loger import write_logs


bot = telebot.TeleBot('5947528384:AAHsWuJ87P9lQV6WdRKU-9QnfhEML9ZDw_0')
data_base = BdHelper()
DELETE_ACCOUNT_TEXT = "Are you sure?"
DELETED_ACCOUNT_TEXT = "Your account has been deleted"
START_ACTIVE_TIME_TEXT = "We will soon find your creative group."
DONT_FOUND_MATCH_TEXT = "Don't wait to start being creative!"
ALREADY_IN_GROUP_TEXT = """You are already in a group. 
You can continue creating in there or you can leave it and find a new match."""
HAVE_NO_ACCOUNT_TEXT = "You don't have an account yet. Create one to start being creative."
APPEND_IN_GROUP_TEXT = "Check the pinned message!"
FIRE_ACOOUNT_TEXT = "You have been on creative fire today. Come back tomorrow."
REMOVED_FROM_GROUP_TEXT = "You have been removed from the group."
ALREADY_STOP_SEARCHING_TEXT = "You already stop to searching"
APPROVE_TO_JOIN_TEXT = "You have been approved to join the chat!"
NEED_TIME_ZONE_TEXT = "I need your timezone"
CHOOSE_TIME_ZONE_TEXT = "Choose your time zone"
INCORRECT__TIME_TEXT = "Start time cannot equal or exceed finish time"
CHOOSE_MOUTION_TEXT = "Choose what you want to do"
STOP_SEARCHING_TEXT = "You have stopped searching"
SET_ACTIVE_TIME_TEXT = "You should to set active time"
LINK_INVITE_TEXT = "Yours link for time"


@bot.message_handler(content_types=['new_chat_members'])
def join_request(update: types.ChatJoinRequest):
    user_id = update.from_user.id
    chat_id = update.chat.id
    bot.send_message(user_id, APPROVE_TO_JOIN_TEXT)
    info = data_base.get_user_info_from_id(user_id)
    data_base.change_active_status(user_id, "False")
    data_base.add_user_to_Active_Chat(user_id, chat_id)
    data_base.upgrade_room_info_append(user_id, info[5], info[6])
    data_base.update_rooms_users_count(chat_id, '+')

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
    data_base.update_rooms_users_count(chat_id, '-')
    bot.send_message(user_id, REMOVED_FROM_GROUP_TEXT)
    print("User left chat")

# If create new chat
@bot.message_handler(commands=['add_chat_into_active'])
def add_chat_into_active(message):
    try:
        chat_id = message.chat.id
        if int(message.from_user.id) == int(243980106):
            data_base.add_chat_into_active(chat_id, message.chat.title)
            bot.send_message(chat_id, "Chat added")
        else:
            bot.send_message(chat_id, "You can't do it")
    except Exception("add_chat_into_active Wrong") as e:
        bot.send_message(chat_id, e)

#  If delete chat
@bot.message_handler(commands=['delete_chat_from_active'])
def delete_chat_from_active(message):
    try:
        chat_id = message.chat.id
        if int(message.from_user.id) == int(243980106):
            data_base.delete_chat_from_active(chat_id)
            bot.send_message(chat_id, "Chat deleted")
        else:
            bot.send_message(chat_id, "You can't do it")
    except Exception("delete_chat_from_active Wrong") as e:
        bot.send_message(chat_id, e)

@bot.message_handler(commands=['start'])
def send_start(message):
    try:
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
        data_base.add_user(message.from_user.id , message.from_user.username)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Set time zone")
        markup.add(item1)
        bot.send_message(message.from_user.id, NEED_TIME_ZONE_TEXT, reply_markup=markup)
    except Exception("Create_Account Wrong") as e:
        bot.send_message(message.from_user.id, e)

def set_time_zone(message):
    try:
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("Info"))
    try:
        item1 = types.KeyboardButton("Set time zone")
        item2 = types.KeyboardButton("Set active time")
        item3 = types.KeyboardButton("Delete account")
        item4 = types.KeyboardButton("Stop searching")
        markup.add(item1, item2, item3, item4)
        msg = CHOOSE_MOUTION_TEXT
    except :
        bot.send_message(message.from_user.id, "menu Wrong")
    bot.send_message(message.from_user.id, msg, reply_markup=markup)

def delete_account(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    try:
        item1 = types.KeyboardButton("Sure")
        item2 = types.KeyboardButton("Menu")
        markup.add(item1, item2)
        bot.send_message(message.from_user.id, DELETE_ACCOUNT_TEXT, reply_markup=markup)
    except Exception("delete_account Wrong") as e:
        bot.send_message(message.from_user.id, e)

def sure(message):
    try:
        id_chat = data_base.loock_user_into_chats(message.from_user.id)
        data_base.update_rooms_users_count(id_chat, "-")
        data_base.delete_user(message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Create account")
        markup.add(item1)
        bot.send_message(message.from_user.id, DELETED_ACCOUNT_TEXT, reply_markup=markup)
    except Exception("Sure Wrong") as e:
        bot.send_message(message.from_user.id, e)

def stop_searching(message):
    try:
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

@bot.message_handler(commands=['Info'])
def info(message):
    try: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton("Menu"))
        bot.send_message(message.from_user.id, "Some info", reply_markup=markup)
    except:
        bot.send_message(message.from_user.id, "Info Wrong")

def set_time_zone_func(message, match, markup):
    
    time_zone = match.group(1)     
    data_base.set_time_zone(message.from_user.id, time_zone)
    bot.send_message(message.from_user.id, f"Done, your time zone: {time_zone}", reply_markup=markup)

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
    bot.send_message(call.chat.id, "Choose time", reply_markup=markup)


def start_time(call, time):
    data_base.set_active_time_start(call.from_user.id, time)

def end_time(call, time):
    data_base.set_active_time_end(call.from_user.id, time)

def start_search(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("Menu"))
    data_base.change_active_status(message.from_user.id, "False")
    time_zone_hours = data_base.get_time_zone(message.from_user.id)
    time_zone = dt.timedelta(hours=time_zone_hours)
    td = dt.date.today()
    person_info = data_base.get_user_info_from_id(message.from_user.id)
    if person_info[5] == None or person_info[6] == None:
        bot.send_message(message.from_user.id, SET_ACTIVE_TIME_TEXT, reply_markup=markup)
        return
    time_start_person = dt.datetime.strptime(person_info[5], '%H:%M').time() 
    time_end_person = dt.datetime.strptime(person_info[6], '%H:%M').time() 
    if time_start_person >= time_end_person:
        bot.send_message(message.from_user.id, INCORRECT__TIME_TEXT, reply_markup=markup)
        return

    time_start = (dt.datetime.combine(td, time_start_person) + time_zone).strftime("%H:%M")
    time_end = (dt.datetime.combine(td, time_end_person) + time_zone).time().strftime("%H:%M")

    user_active = data_base.loock_user_into_chats(message.from_user.id)
    if user_active:
        bot.send_message(message.from_user.id, ALREADY_IN_GROUP_TEXT, reply_markup=markup)
        return
    data_base.set_active_time_start(message.from_user.id, time_start)
    data_base.set_active_time_end(message.from_user.id, time_end)
    bot.send_message(message.from_user.id, START_ACTIVE_TIME_TEXT, reply_markup=markup)
    data_base.change_active_status(message.from_user.id, "True")
    users = data_base.get_match(time_start, time_end)
    if len(users) > 1:
        active_users = data_base.get_active_users(time_start, time_end)
        chat_id, name_room = data_base.get_free_room_id(time_start, time_end)
        if chat_id == 0:
            bot.send_message(message.from_user.id, "No free rooms")
            return
        link = bot.create_chat_invite_link(chat_id= chat_id, name=name_room, expire_date= dt.datetime.now()+dt.timedelta(minutes=30))
        for user in active_users:
            bot.send_message(user[0], f"{LINK_INVITE_TEXT}  {user[2]}-{user[3]}", reply_markup=markup)
            bot.send_message(user[0], link.invite_link)
    else:
        bot.send_message(message.from_user.id, DONT_FOUND_MATCH_TEXT, reply_markup=markup)

def check_persons(message, markup):
    try:
        info = data_base.get_info_all_users_in_chats()
        html = ""
        for i in info:
            user = f"""name: {i[1]}  id: {i[0]}   time_zone: {i[2]} id_chat:{i[3]}   name_chat: {i[4]} 
s_time: {i[5]}   e_time {i[6]}"""
            html = html + user + "\n"
        bot.send_message(message.from_user.id, html, reply_markup=markup)
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
        have_not_account(call)

def have_not_account(message):
    markap = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markap.add(types.KeyboardButton("Info"))
    markap.add(types.KeyboardButton("Create account"))
    bot.send_message(message.from_user.id, HAVE_NO_ACCOUNT_TEXT, reply_markup=markap)

@bot.message_handler(content_types='text')
def text_holder(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    match = re.search(r'Set time zone ([-+]\d) UTC', message.text)     
    if message.text not in ["Info", "Create account"] and data_base.get_one_user(message.from_user.id) is None:
        have_not_account(message)
        return
    markup.add(types.KeyboardButton("Menu")) 
    if match:
        set_time_zone_func(message, match, markup)
    elif message.text == "Menu":
        menu(message)
    elif message.text == "Set time zone":
        set_time_zone(message) 
    elif message.text == "Set active time":
        set_active_time_panel(message)
    elif message.text == "Delete account":
        delete_account(message)
    elif message.text == "Info":
        info(message)
    elif message.text == "Sure":
        sure(message)
    elif message.text == "Create account":
        create_account(message)
    elif message.text == "Stop searching":
        stop_searching(message)
    elif message.text == "Check persons":
        if int(message.from_user.id) in [243980106, 402816936]:
            check_persons(message, markup)



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
            bot.send_message(243980106, f"Dangerous_Error: {e}")
            write_logs(f"Dangerous_Error: {e}", folder="error_logs")
