-- SQLite
CREATE VIEW IF NOT EXISTS view_persons_in_chats AS
SELECT user_id, user_name, time_zone, Chats.id_chat, Chats.name, user_time_start, user_time_end
FROM ReadyUsers, Active_Chat, Chats
WHERE ReadyUsers.user_id = Active_Chat.id_user
AND Active_Chat.id_chat = Chats.id_chat;