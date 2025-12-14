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
    sql = """ SELECT id, title, content, price, genre, user_id FROM posts ORDER BY id DESC;
    """
    rivit= db.query(sql)
    return [{"id": r["id"], "title": r["title"], "content": r["content"], "price": r["price"], "genre": r["genre"], "user_id": r["user_id"]} for r in rivit]

def get_item(id):
    sql = """
        SELECT posts.id, posts.title, posts.content, posts.price, posts.genre, users.username, posts.user_id
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = ?
    """
    result = db.query(sql, [id])
    return result[0] if result else None

def update_item(id, title, content, price, genre, user_id):
    sql = "UPDATE posts SET title=?, content=?, price=?, genre=?, user_id=? WHERE id=?"
    db.execute(sql, [title, content, price, genre, user_id, id])

def delete_item(id):
    sql = "DELETE FROM posts WHERE id=?"
    db.execute(sql, [id])

def get_posts_by_user(user_id):
    sql = """ SELECT id, title, content, price, genre FROM posts WHERE user_id = ? ORDER BY id DESC;
    """
    rivit= db.query(sql, [user_id])
    return [{"id": r["id"], "title": r["title"], "content": r["content"], "price": r["price"], "genre": r["genre"]} for r in rivit]

def get_user_by_id(id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [id])
    return result[0] if result else None

def find_items(title):
        sql = """SELECT id, title
        FROM posts
        WHERE title LIKE ? or  content like ?
        ORDER BY id DESC"""
        like = "%" + title + "%"
        result = db.query(sql, [like, like])
        return result

def create_rating(post_id, user_id, rating, comment):
    sql = "INSERT INTO ratings (post_id, user_id, rating, comment) VALUES (?, ?, ?, ?)"
    db.execute(sql, [post_id, user_id, rating, comment])

def get_ratings(post_id):
    sql = """
        SELECT ratings.id, ratings.rating, ratings.comment, ratings.user_id, users.username
        FROM ratings
        JOIN users ON ratings.user_id = users.id
        WHERE ratings.post_id = ?
        ORDER BY ratings.id DESC
    """
    return db.query(sql, [post_id])

def get_average_rating(post_id):
    sql = "SELECT AVG(rating) as avg_rating FROM ratings WHERE post_id = ?"
    result = db.query(sql, [post_id])
    return result[0]["avg_rating"] if result else None

def user_has_rated(post_id, user_id):
    sql = "SELECT id FROM ratings WHERE post_id = ? AND user_id = ?"
    return db.query(sql, [post_id, user_id])

def get_user_ratings(user_id):
    sql = """
        SELECT ratings.id, ratings.rating, ratings.comment, posts.title, posts.id as post_id
        FROM ratings
        JOIN posts ON ratings.post_id = posts.id
        WHERE ratings.user_id = ?
        ORDER BY ratings.id DESC
    """
    return db.query(sql, [user_id])

def update_rating(rating_id, rating, comment):
    sql = "UPDATE ratings SET rating=?, comment=? WHERE id=?"
    db.execute(sql, [rating, comment, rating_id])

def get_rating(rating_id):
    sql = "SELECT id, post_id, user_id, rating, comment FROM ratings WHERE id = ?"
    result = db.query(sql, [rating_id])
    return result[0] if result else None

def delete_rating(rating_id):
    sql = "DELETE FROM ratings WHERE id=?"
    db.execute(sql, [rating_id])