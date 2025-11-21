import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
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
    if not item:
        abort(404)
    ratings = items.get_ratings(id)
    avg_rating = items.get_average_rating(id)
    return render_template("item.html", item=item, ratings=ratings, avg_rating=avg_rating)

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
    if not item:
        abort(404)
    if item["user_id"] !=session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/update_item/<int:id>", methods=["POST"])
def update_item(id):

    item = items.get_item(id)
    if not item:
        abort(404)
    if item["user_id"] !=session["user_id"]:
        abort(403)

    title=request.form["title"]
    content=request.form["content"]
    price=request.form.get("price", 0)
    genre=request.form.get("genre", "Muu")
    user_id=session["user_id"]
    items.update_item(id, title, content, price, genre, user_id)
    return redirect("/item/"+str(id))

@app.route("/delete_item/<int:id>",methods = ["GET","POST"])
def delete_item(id):
    item = items.get_item(id)
    if not item:
        abort(404)
    if item["user_id"] !=session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("delete_item.html", item=item)
    if "remove" in request.form:
        items.delete_item(id)
        return redirect("/")
    else:
        return redirect("/item/"+str(id))



@app.route("/find_item", methods=["GET","POST"])
def find_item():
    title = request.args.get("title", "")
    if title:
        results = items.find_items(title)
    else:
        title = " "
        results = []
    title = request.args.get("title")
    return render_template("find_item.html", title=title, results=results)




@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("register_failure.html", message="Salasanat eivät täsmää")
    password_hash = generate_password_hash(password1)

    try:
        items.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        return render_template("register_failure.html", message="Tunnus on jo varattu")

    return render_template("register_success.html")




@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        result = items.get_user(username)
        
        if not result:
            return "VIRHE: väärä tunnus tai salasana"
        
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/user_page/<int:id>")
def user_page(id):
    user = items.get_user_by_id(id)
    if not user:
        abort(404)
    posts = items.get_posts_by_user(id)
    ratings = items.get_user_ratings(id)
    return render_template("user_page.html", user=user, posts=posts, ratings=ratings)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/rate_item/<int:id>", methods=["POST"])
def rate_item(id):
    if "user_id" not in session:
        abort(403)
    item = items.get_item(id)
    if not item:
        abort(404)
    if item["user_id"] == session["user_id"]:
        abort(403) 

    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment", "")
    
    if not (1 <= rating <= 5):
        abort(400)
    
    try:
        items.create_rating(id, session["user_id"], rating, comment)
    except sqlite3.IntegrityError:
        return "Olet jo arvioinut tämän pelin"
    
    return redirect("/item/"+str(id))