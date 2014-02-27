from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        #return "User %s is logged in!" % session['username']
        return redirect(url_for("user_wall",username=session['username']))
    else:
        return render_template("index.html")
    # return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    model.connect_to_db()
    username = request.form.get("username")
    password = request.form.get("password")

    if model.authenticate(username, password):
        flash("User authenticated")
        session['username'] = username
    else:
        flash("Password incorrect, there may be a ferret stampede in progress. Save yourself!")
        
    return redirect(url_for("index"))


@app.route("/logout")
def clear_session():
    session.clear()
    flash("You logged out.")
    print "You logged out!!"
    #call session.clear() method
    return redirect(url_for("index"))

@app.route("/register")
def register():
    if session.get("username"):
        return redirect(url_for("user_wall",username=session['username']))
    else:
        return render_template("register.html")

@app.route("/register", methods=["POST"])     
def register_user():
    model.connect_to_db()
    username = request.form.get("username")
    password = request.form.get("password")
    password_verify = request.form.get("password_verify")
    response = model.create_account(username, password, password_verify)
    if response == 1:
        flash("That name is already in use. Please try again.")
        return redirect(url_for("register"))
    elif response == 2:
        flash("Passwords do not match. Please try again.")
        return redirect(url_for("register"))
    else:
        flash("Success! Please log in to view your wall.")
        return redirect(url_for("index"))


@app.route("/user/<username>")
def user_wall(username):
    model.connect_to_db()
    user_id = model.get_userid_by_name(username)
    wall_posts = model.get_wall_posts(user_id)
    html = render_template("wall.html", username=username, wall_posts=wall_posts)
    return html

@app.route("/user/<username>", methods=["POST"])
def post_to_wall(username):
    model.connect_to_db()
    user_id = model.get_userid_by_name(username)
    wall_posts = model.get_wall_posts(user_id)    
    author_id = model.get_userid_by_name(session.get("username"))
    wall_owner = username
    content = request.form.get("content")
    model.post_to_wall(wall_owner, author_id, content)
    return redirect(url_for("user_wall",username=username))

if __name__ == "__main__":
    app.run(debug = True)
