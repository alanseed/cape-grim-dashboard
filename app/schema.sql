DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS obs_data;
DROP TABLE IF EXISTS obs_names;
DROP TABLE IF EXISTS charts;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL,
  role TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE obs_data ( 
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  obs_id INTEGER FOREIGN KEY,
  obs_time INTEGER, 
  obs REAL 
)

CREATE_TABLE obs_names(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  obs_name TEXT UNIQUE NOT NULL, 
)

CREATE TABLE charts ( 
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  show INTEGER NOT NULL,
  char_name TEXT NOT NULL, 
  obs_list TEXT NOT NULL,
  title TEXT, 
  time_format TEXT,
  left_title TEXT, 
  left_log INTEGER, 
  left_min  REAL, 
  left_max REAL, 
  right_title TEXT,
  right_log INTEGER, 
  right_min REAL, 
  right_max REAL
)