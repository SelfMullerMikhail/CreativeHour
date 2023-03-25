-- SQLite
-- SQLite
-- DROP TABLE IF EXISTS Active_Chat;
-- CREATE TABLE IF NOT EXISTS Active_Chat (
-- id INTEGER PRIMARY KEY AUTOINCREMENT,
-- id_chat TEXT NOT NULL,
-- id_user INT NOT NULL,
-- FOREIGN KEY (id_user) REFERENCES ReadyUsers(`user_id`),
-- FOREIGN KEY (id_chat) REFERENCES Chats(`id_chat`)
-- );

DELETE FROM Active_Chat WHERE id = 5;
DELETE FROM Active_Chat WHERE id = 8;
DELETE FROM Active_Chat WHERE id = 11;