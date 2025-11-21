CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    price REAL,
    user_id INTEGER REFERENCES users(id),
    genre TEXT
);

CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    user_id INTEGER REFERENCES users(id),
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    UNIQUE(post_id, user_id)
);