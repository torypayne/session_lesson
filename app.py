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
    return render_template("register.html")

@app.route("/user/<username>")
def user_wall(username):
    #take username, look up user_id
    #to do this, write get_user_by_name func in model.py
    #call this function
    #use user_id to look up wall_posts
    #return posts/rows to wall.html
    model.connect_to_db()
    user_id = model.get_userid_by_name(username)
    wall_posts = model.get_wall_posts(user_id)
    html = render_template("wall.html", username=username, wall_posts=wall_posts)
    return html


if __name__ == "__main__":
    app.run(debug = True)
