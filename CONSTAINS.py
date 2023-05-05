import os
from json_function import JsonConnector

# from test import API_TEST
# # API = API_TEST

js_helper = JsonConnector()
VERSION = "Version 9"
START_TIME = "\n\nStart time - End time"
API = os.getenv('API')
BUCKET_NAME = os.getenv('BUCKET_NAME')
TIME_FIRE =lambda: js_helper.get_constains("TIME_FIRE")
PUSHING_TIME =lambda: js_helper.get_constains("PUSHING_TIME")
ADMIN_IP_MISHA =lambda: js_helper.get_constains("ADMIN_IP_MISHA")
ADMIN_IP_ASYA =lambda: js_helper.get_constains("ADMIN_IP_ASYA")
TOTAL_ADMINS =lambda: js_helper.get_constains("TOTAL_ADMINS")
WELCOME_MESSAGE =lambda: js_helper.get_constains("WELCOME_MESSAGE")
KICK_MESSAGE = lambda: js_helper.get_constains("KICK_MESSAGE")
APROVE_MESSAGE = lambda: js_helper.get_constains("APROVE_MESSAGE")
MORNING_MESSAGE = lambda:js_helper.get_constains("MORNING_MESSAGE")
DELETE_ACCOUNT_TEXT = lambda:js_helper.get_constains("DELETE_ACCOUNT_TEXT")
DELETED_ACCOUNT_TEXT = lambda:js_helper.get_constains("DELETED_ACCOUNT_TEXT")
START_ACTIVE_TIME_TEXT = lambda:js_helper.get_constains("START_ACTIVE_TIME_TEXT")
DONT_FOUND_MATCH_TEXT = lambda:js_helper.get_constains("DONT_FOUND_MATCH_TEXT")
ALREADY_IN_GROUP_TEXT = lambda:js_helper.get_constains("ALREADY_IN_GROUP_TEXT")
HAVE_NO_ACCOUNT_TEXT = lambda:js_helper.get_constains("HAVE_NO_ACCOUNT_TEXT")
APPEND_IN_GROUP_TEXT = lambda:js_helper.get_constains("APPEND_IN_GROUP_TEXT")
FIRE_ACOOUNT_TEXT = lambda:js_helper.get_constains("FIRE_ACOOUNT_TEXT")
REMOVED_FROM_GROUP_TEXT = lambda:js_helper.get_constains("REMOVED_FROM_GROUP_TEXT")
ALREADY_STOP_SEARCHING_TEXT = lambda:js_helper.get_constains("ALREADY_STOP_SEARCHING_TEXT")
APPROVE_TO_JOIN_TEXT = lambda:js_helper.get_constains("APPROVE_TO_JOIN_TEXT")
NEED_TIME_ZONE_TEXT = lambda:js_helper.get_constains("NEED_TIME_ZONE_TEXT")
CHOOSE_TIME_ZONE_TEXT = lambda:js_helper.get_constains("CHOOSE_TIME_ZONE_TEXT")
INCORRECT__TIME_TEXT = lambda:js_helper.get_constains("INCORRECT__TIME_TEXT")
CHOOSE_MOUTION_TEXT = lambda:js_helper.get_constains("CHOOSE_MOUTION_TEXT")
STOP_SEARCHING_TEXT = lambda:js_helper.get_constains("STOP_SEARCHING_TEXT")
SET_ACTIVE_TIME_TEXT = lambda:js_helper.get_constains("SET_ACTIVE_TIME_TEXT")
LINK_INVITE_TEXT = lambda:js_helper.get_constains("LINK_INVITE_TEXT")
INFO_TEXT = lambda:js_helper.get_constains("INFO_TEXT")
JOIN_GROUP_TEXT = lambda:js_helper.get_constains("JOIN_GROUP_TEXT")
FIRST_MESSAGE_GROUP = lambda:js_helper.get_constains("FIRST_MESSAGE_GROUP")
INSTRUCTION_FOR_SET_ACTIVE_TIME =lambda: js_helper.get_constains("INSTRUCTION_FOR_SET_ACTIVE_TIME")
DELETE_FROM_GROUP = lambda: js_helper.get_constains("DELETE_FROM_GROUP")