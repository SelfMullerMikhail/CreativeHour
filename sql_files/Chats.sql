DROP TABLE IF EXISTS Chats;
CREATE TABLE Chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_chat INTEGER NOT NULL,
    name TEXT NOT NULL,
    max_users INTEGER NOT NULL,
    users_now INTEGER NOT NULL DEFAULT 0,
    min_start_time DATETIME DEAFULT 'None',
    max_end_time DATETIME DEFAULT 'None'
);


INSERT INTO Chats (id_chat, name, max_users, min_start_time, max_end_time) 
VALUES (-1001507918351, 'Chat_1', 3, 'None', 'None');

-- SELECT *
-- FROM Chats
-- WHERE max_users >= users_now 
-- AND (min_start_time <= '10:00' AND max_start_time <= '12:00');