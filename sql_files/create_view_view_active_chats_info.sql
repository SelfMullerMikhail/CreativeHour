-- -- SQLite
-- DROP VIEW IF EXISTS view_active_chats_info;
-- CREATE VIEW view_active_chats_info AS 
-- SELECT Chats.id_chat, ReadyUsers.user_id, ReadyUsers.user_time_start, ReadyUsers.user_time_end
-- FROM Active_Chat, Chats, ReadyUsers
-- WHERE Active_Chat.id_chat = Chats.id_chat
-- AND Active_Chat.id_user = ReadyUsers.user_id;

SELECT min(user_time_start), max(user_time_end)
FROM view_active_chats_info
WHERE id_chat = 1;