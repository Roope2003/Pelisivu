import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import items
import db
import config
app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    posts=items.get_all_posts()
    return render_template("index.html", posts=posts)


@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/item/<int:id>")
def show_item(id):
    item = items.get_item(id)
    return render_template("item.html", item=item)


@app.route("/create_item", methods=["POST"])
def create_item():
    title = request.form["title"]
    content = request.form["content"]
    price = request.form.get("price", 0)
    genre = request.form.get("genre", "Muu")
    user_id = session["user_id"]
    items.create_post(title, content, price, user_id, genre)
    return redirect("/")


@app.route("/edit_item/<int:id>")
def edit_item(id):
    item = items.get_item(id)
    return render_template("edit_item.html", item=item)

@app.route("/update_item/<int:id>", methods=["POST"])
def update_item(id):
    title=request.form["title"]
    content=request.form["content"]
    price=request.form.get("price", 0)
    genre=request.form.get("genre", "Muu")
    user_id=session["user_id"]
    items.update_item(id, title, content, price, genre, user_id)
    return redirect("/item/"+str(id))

@app.route("/delete_item/<int:id>")
def delete_item(id):
    items.delete_item(id)
    return redirect("/")





@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        items.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"




@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method=="POST":
            username = request.form["username"]
            password = request.form["password"]
            result = items.get_user(username)
            user_id = result["id"]
            password_hash = result["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"] = user_id
                session["username"] = username
                return redirect("/")
            else:
                return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")