from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        return "User %s is logged in!" % session['username']
    else:
        return render_template("index.html")
    # return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    # username = model.authenticate(username, password)
    # if username != None:
    #     flash('message') = "User authenticated!"
    #     session['username'] = username
    # else:
    #     flash('message') = "Password incorrect, there may be a ferret stampede in progress. Save yourself!"

    # return redirect(url_for("index"))
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

if __name__ == "__main__":
    app.run(debug = True)
