import sqlite3
import db

def create_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def get_user(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0] if result else None

def create_post(title, content, price, user_id, genre):
    sql = "INSERT INTO posts (title, content, price, user_id, genre) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, content, price, user_id, genre])

def get_all_posts():
    sql = """ SELECT id, title, content, price, user_id FROM posts ORDER BY id DESC;
    """
    rivit= db.query(sql)
    return [{"id": r["id"], "title": r["title"]} for r in rivit]

def get_item(id):
    sql = """
        SELECT posts.id, posts.title, posts.content, posts.price, posts.genre, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = ?
    """
    result = db.query(sql, [id])
    return result[0] if result else None
