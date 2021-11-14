DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL,
  role TEXT NOT NULL,
  password TEXT NOT NULL
);