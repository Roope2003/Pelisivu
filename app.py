import sqlite3
import secrets
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import items
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.context_processor
def inject_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return {"csrf_token": session["csrf_token"]}

@app.before_request
def csrf_protect():
    if request.method == "POST" and request.endpoint not in ("login",):
        session_token = session.get("csrf_token")
        form_token = request.form.get("csrf_token")
        if not session_token or session_token != form_token:
            abort(403)
def require_login():
    if "user_id" not in session:
        abort(403)

def verify_owner(obj):
    if not obj:
        abort(404)
    if obj["user_id"] !=session["user_id"]:
        abort(403)



@app.route("/")
def index():
    posts=items.get_all_posts()
    return render_template("index.html", posts=posts)


@app.route("/new_item")
def new_item():
    require_login()
    return render_template("new_item.html")

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)

    ratings = items.get_ratings(item_id)
    avg_rating = items.get_average_rating(item_id)
    return render_template("item.html", item=item, ratings=ratings, avg_rating=avg_rating)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()

    title = request.form["title"]
    content = request.form["content"]
    price = request.form.get("price", 0)
    genres = request.form.getlist("genre")
    genre = ",".join([g for g in genres])
    user_id = session["user_id"]

    items.create_post(title, content, price, user_id, genre)
    return redirect("/")


@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    verify_owner(item)
    return render_template("edit_item.html", item=item)

@app.route("/update_item/<int:item_id>", methods=["POST"])
def update_item(item_id):
    require_login()
    item = items.get_item(item_id)
    verify_owner(item)

    title=request.form["title"]
    content=request.form["content"]
    price=request.form.get("price", 0)
    genres = request.form.getlist("genre")
    genre = ",".join([g for g in genres])
    user_id=session["user_id"]
    item_data = {"title": title, "content": content, "price": price, "genre": genre,
                "user_id": user_id,}
    items.update_item(item_id,item_data)
    return redirect("/item/"+str(item_id))

@app.route("/delete_item/<int:item_id>", methods=["GET", "POST"])
def delete_item(item_id):
    require_login()
    item = items.get_item(item_id)
    verify_owner(item)

    if request.method == "GET":
        return render_template("delete_item.html", item=item)
    if "remove" in request.form:
        items.delete_item(item_id)
        return redirect("/")
    else:
        return redirect("/item/"+str(item_id))



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
            return render_template("login_failure.html")

        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login_failure.html")

@app.route("/user_page/<int:user_id>")
def user_page(user_id):
    user = items.get_user_by_id(user_id)

    if not user:
        abort(404)

    posts = items.get_posts_by_user(user_id)
    ratings = items.get_user_ratings(user_id)
    return render_template("user_page.html", user=user, posts=posts, ratings=ratings)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/rate_item/<int:item_id>", methods=["POST"])
def rate_item(item_id):
    require_login()
    item = items.get_item(item_id)

    if not item:
        abort(404)

    if item["user_id"] == session["user_id"]:
        abort(403)

    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment", "")
    if not 1 <= rating <= 5:
        abort(400)

    try:
        items.create_rating(item_id, session["user_id"], rating, comment)
    except sqlite3.IntegrityError:

        current_rating = items.user_has_rated(item_id, session["user_id"])
        rating_id = current_rating[0]["id"]

        return render_template("rating_failure.html", rating_id=rating_id)

    return redirect("/item/"+str(item_id))

@app.route("/edit_rating/<int:rating_id>", methods=["GET", "POST"])
def edit_rating(rating_id):
    require_login()
    rating = items.get_rating(rating_id)
    verify_owner(rating)

    if request.method == "GET":
        return render_template("edit_rating.html", rating=rating)

    rating_val = request.form.get("rating", type=int)
    comment = request.form.get("comment", "")

    if not 1 <= rating_val <= 5:
        abort(400)

    items.update_rating(rating_id, rating_val, comment)
    return redirect("/item/" + str(rating["post_id"]))

@app.route("/delete_rating/<int:rating_id>", methods=["GET", "POST"])
def delete_rating(rating_id):
    require_login()
    rating = items.get_rating(rating_id)
    verify_owner(rating)

    if request.method == "GET":
        return render_template("delete_rating.html", rating=rating)

    if "remove" in request.form:
        items.delete_rating(rating_id)

    return redirect("/item/" + str(rating["post_id"]))
