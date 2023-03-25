-- -- SQLite
DROP TABLE IF EXISTS ReadyUsers;
CREATE TABLE ReadyUsers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL UNIQUE,
    user_name TEXT NOT NULL,
    time_zone TEXT DEFAULT '+0',
    user_hobby TEXT DEFAULT 'None',
    user_time_start time,
    user_time_end time,
    ready_flag TEXT DEFAULT 'False'
);

-- -- SQLite
INSERT INTO ReadyUsers (user_id, user_name, time_zone)
VALUES (243980106, 'arkravchenko', '+3');

INSERT INTO ReadyUsers (user_id, user_name, time_zone)
VALUES (402816936, 'Mihail_Muller', '+0');

INSERT INTO ReadyUsers (user_id, user_name, time_zone)
VALUES (5726717629, 'None', '+0');