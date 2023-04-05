-- SQLite
-- создание таблицы Chats
DROP TABLE IF EXISTS Chats;
CREATE TABLE Chats (
    id SERIAL PRIMARY KEY,
    id_chat TEXT NOT NULL,
    name TEXT NOT NULL,
    max_users INTEGER NOT NULL,
    users_now INTEGER NOT NULL DEFAULT 0,
    min_start_time TIMESTAMP DEFAULT NULL,
    max_end_time TIMESTAMP DEFAULT NULL
);

-- создание таблицы ReadyUsers
DROP TABLE IF EXISTS ReadyUsers;
CREATE TABLE ReadyUsers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    user_name TEXT NOT NULL,
    time_zone TEXT DEFAULT '+0',
    user_hobby TEXT DEFAULT 'None',
    user_time_start TIME,
    user_time_end TIME,
    ready_flag TEXT DEFAULT 'False'
);

-- создание таблицы Active_Chat
DROP TABLE IF EXISTS Active_Chat;
CREATE TABLE IF NOT EXISTS Active_Chat (
    id SERIAL PRIMARY KEY,
    id_chat TEXT NOT NULL,
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES ReadyUsers(user_id),
    FOREIGN KEY (id_chat) REFERENCES Chats(id_chat)
);

-- создание представления view_active_chats_info
DROP VIEW IF EXISTS view_active_chats_info;
CREATE VIEW view_active_chats_info AS 
SELECT Chats.id_chat, ReadyUsers.user_id, ReadyUsers.user_time_start, ReadyUsers.user_time_end
FROM Active_Chat, Chats, ReadyUsers
WHERE Active_Chat.id_chat = Chats.id_chat
AND Active_Chat.id_user = ReadyUsers.user_id;

-- создание представления view_persons_in_chats
CREATE VIEW IF NOT EXISTS view_persons_in_chats AS
SELECT user_id, user_name, time_zone, Chats.id_chat, Chats.name, user_time_start, user_time_end
FROM ReadyUsers, Active_Chat, Chats
WHERE ReadyUsers.user_id = Active_Chat.id_user
AND Active_Chat.id_chat = Chats.id_chat;

-- добавление записей в таблицу Chats
INSERT INTO Chats (name, id_chat, max_users)
VALUES ('AsyaBotChat_1', '-1001766992539', 5),
       ('AsyaBotChat_2', '-1001941589630', 5),
       ('AsyaBotChat_3', '-1001988286731', 5);

-- удаление записей из таблицы Active_Chat
DELETE FROM Active_Chat WHERE id IN (5, 8, 11);
