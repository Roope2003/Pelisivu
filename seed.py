import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM posts")
db.execute("DELETE FROM ratings")

user_count = 100000
post_count = 10**6
rating_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, post_count + 1):

    title = f"game{i}"
    content = "test content"
    price = 4.20
    user_id = random.randint(1, user_count)
    genre = "RPG"

    title = "game" + str(i)
    sql = """
    INSERT INTO posts (title, content, price, user_id, genre)
    VALUES (?, ?, ?, ?, ?)
    """
    db.execute(sql, [title, content, price, user_id, genre])

for i in range(1, rating_count + 1):
    user_id = random.randint(1, user_count)
    post_id = random.randint(1, post_count)
    rating= "1"
    comment="test"
    db.execute("INSERT  OR IGNORE INTO ratings (post_id, user_id, rating, comment) VALUES (?, ?, ?, ?)"
            ,
            [post_id, user_id,rating, comment])






db.commit()
db.close()
