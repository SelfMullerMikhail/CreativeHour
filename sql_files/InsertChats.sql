-- SQLite
-- # Group_1 = "-933165519"
-- # Group_2 = "-1001941589630"
-- # Group_3 = "-1001988286731"

-- INSERT INTO Chats(id, name, id_chat, max_users) 
-- VALUES (1, 'AsyaBotChat_1', '-1001766992539', 3);

-- INSERT INTO Chats (name, id_chat, max_users)
-- VALUES ("AsyaBotChat_2", "-1001941589630", 3);

-- INSERT INTO Chats (name, id_chat, max_users)
-- VALUES ("AsyaBotChat_3", "-1001988286731", 3);

-- UPDATE Chats SET min_start_time = 'None' WHERE id = 1;
-- UPDATE Chats SET max_end_time = 'None' WHERE id = 1;
-- UPDATE Chats SET users_now = '0' WHERE id = 1;

-- UPDATE Chats SET min_start_time = 'None' WHERE id = 2;
-- UPDATE Chats SET max_end_time = 'None' WHERE id = 2;
-- UPDATE Chats SET users_now = '0' WHERE id = 2;

-- UPDATE Chats SET min_start_time = 'None' WHERE id = 3;
-- UPDATE Chats SET max_end_time = 'None' WHERE id = 3;
-- UPDATE Chats SET users_now = '0' WHERE id = 3;

-- UPDATE ReadyUsers SET user_time_start = '09:00' WHERE id = 11;
-- UPDATE ReadyUsers SET user_time_end = '11:00' WHERE id = 11;

DELETE FROM Active_Chat WHERE id = 1;

DELETE FROM ReadyUsers WHERE id = 5;
DELETE FROM ReadyUsers WHERE id = 11;