CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT ,
    content TEXT ,
    price REAL,
    user_id REFERENCES users ,
    genre TEXT
);