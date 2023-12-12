import os
import math

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///last_fm.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    message = None
    criteria = 0
    if request.method == "GET":
        return render_template("index.html", message=message)
    else:
        temp1 = []
        temp2 = []
        temp3 = []
        result = []
        song_dict = []
        saved_songs = []
        now_saved_songs = []
        new_songs = []
        # For popularity
        if request.form.get("popularity"):
            popularity_ap = db.execute("SELECT id FROM FEATURES_2 WHERE track_popularity BETWEEN ? AND ?",
                                       int(request.form.get("popularity")) - 7, int(request.form.get("popularity")) + 7)
            temp1.append(popularity_ap)
            criteria = criteria + 1
        # For tempo
        if request.form.get("tempo"):
            tempo = float(request.form.get("tempo"))
            tempo_ap = db.execute("SELECT id FROM FEATURES_2 WHERE tempo BETWEEN ? AND ?",
                                  math.floor(tempo) - 10, math.ceil(tempo) + 10)
            temp1.append(tempo_ap)
            criteria = criteria + 1
        # For valence
        if request.form.get("valence"):
            valence = float(request.form.get("valence"))
            valence_ap = db.execute("SELECT id FROM FEATURES_2 WHERE valence BETWEEN ? AND ?", valence - 0.075, valence + 0.075)
            temp1.append(valence_ap)
            criteria = criteria + 1
        # For danceability
        if request.form.get("danceability"):
            danceability = float(request.form.get("danceability"))
            danceability_ap = db.execute("SELECT id FROM FEATURES_2 WHERE danceability BETWEEN ? AND ?",
                                         danceability - 0.075, danceability + 0.075)
            temp1.append(danceability_ap)
            criteria = criteria + 1
        # For energy
        if request.form.get("energy"):
            energy = float(request.form.get("energy"))
            energy_ap = db.execute("SELECT id FROM FEATURES_2 WHERE energy BETWEEN ? AND ?", energy - 0.075, energy + 0.075)
            temp1.append(energy_ap)
            criteria = criteria + 1
        # For acousticness
        if request.form.get("acousticness"):
            acousticness = float(request.form.get("acousticness"))
            acousticness_ap = db.execute("SELECT id FROM FEATURES_2 WHERE acousticness BETWEEN ? AND ?",
                                         acousticness - 0.075, acousticness + 0.075)
            temp1.append(acousticness_ap)
            criteria = criteria + 1
        # For liveness
        if request.form.get("liveness"):
            liveness = float(request.form.get("liveness"))
            liveness_ap = db.execute("SELECT id FROM FEATURES_2 WHERE liveness BETWEEN ? AND ?", liveness - 0.075, liveness + 0.075)
            temp1.append(liveness_ap)
            criteria = criteria + 1
        # For instrumentalness
        if request.form.get("instrumentalness"):
            instrumentalness = float(request.form.get("instrumentalness"))
            instrumentalness_ap = db.execute("SELECT id FROM FEATURES_2 WHERE instrumentalness BETWEEN ? AND ?",
                                             instrumentalness - 0.075, instrumentalness + 0.075)
            temp1.append(instrumentalness_ap)
            criteria = criteria + 1
        # For speechiness
        if request.form.get("speechiness"):
            speechiness = float(request.form.get("speechiness"))
            speechiness_ap = db.execute("SELECT id FROM FEATURES_2 WHERE speechiness BETWEEN ? AND ?",
                                        speechiness - 0.075, speechiness + 0.075)
            temp1.append(speechiness_ap)
            criteria = criteria + 1
        # Make sure that more than three criteria are choosen
        if (criteria < 3):
            message = "Please select at least three criteria"
            return render_template("index.html", message=message)
        for j in range(len(temp1)):
            for n in range(len(temp1[j])):
                temp2.append(temp1[j][n]["id"])
            temp3.append(temp2)
            temp2 = []
        result = temp3[0]
        for m in range(len(temp3) - 1):
            result = set(result).intersection(temp3[m + 1])
        result = list(result)
        # Make sure there are songs to print out
        if len(result) == 0:
            message = "No songs were found"
            return render_template("results.html", message=message)
        else:
            saved_songs_temp = db.execute("SELECT song_id FROM user_songs WHERE user_id = ?", session["user_id"])
            for g in range(len(saved_songs_temp)):
                saved_songs.append(saved_songs_temp[g]["song_id"])
            for b in range(len(result)):
                song_dict.append(db.execute("SELECT * FROM FEATURES_2 WHERE id = ?", result[b]))
            for v in range(len(song_dict)):
                for d in range(len(song_dict[v])):
                    # Because there will be no save button for already saved songs
                    if song_dict[v][d]["id"] in saved_songs:
                        now_saved_songs.append(song_dict[v][d])
                    else:
                        new_songs.append(song_dict[v][d])
            return render_template("results.html", new_songs=new_songs, now_saved_songs=now_saved_songs, message=None)


@app.route("/results", methods=["GET", "POST"])
def mylist():
    if request.method == "POST":
        if request.form.get("add_song"):
            if db.execute("SELECT song_id FROM user_songs WHERE song_id = ? AND user_id = ?", request.form.get("add_song"), session["user_id"]):
                return ('', 204)
            else:
                db.execute("INSERT INTO user_songs (song_id, user_id) VALUES (?, ?)",
                           request.form.get("add_song"), session["user_id"])
        return ('', 204)
    else:
        return render_template("index.html", message=None)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    user_songs = []
    temp1 = []
    song_ids = db.execute("SELECT DISTINCT song_id FROM user_songs WHERE user_id = ?", session["user_id"])
    if len(song_ids) == 0:
        message = "No songs were saved"
        return render_template("dashboard.html", message=message)
    else:
        for i in range(len(song_ids)):
            temp1 = db.execute("SELECT * FROM FEATURES_2 WHERE id = ?", song_ids[i]["song_id"])
            user_songs.append(temp1)
        if request.form.get("rm_song"):
            db.execute("DELETE FROM user_songs WHERE user_id = ? AND song_id = ?", session["user_id"], request.form.get("rm_song"))
            return redirect("/dashboard")
    return render_template("dashboard.html", user_songs=user_songs)


@app.route("/login", methods=["GET", "POST"])
def login():
    message2 = None
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            message2 = "Must provide username"
            return render_template("login.html", message2=message2)

        # Ensure password was submitted
        elif not request.form.get("password"):
            message2 = "Must provide password"
            return render_template("login.html", message2=message2)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            message2 = "Invalid username and/or password"
            return render_template("login.html", message2=message2)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", message2=message2)


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    message1 = None
    """Register user"""
    # TODO: Add the user's entry into the database
    if request.method == "POST":
        # Remember which user has logged in
        if not request.form.get("username"):
            message1 = "Must provide username"
            return render_template("register.html", message1=message1)
        # Ensure password was submitted
        elif not request.form.get("password"):
            message1 = "Must provide password"
            return render_template("register.html", message1=message1)

        elif (db.execute("SELECT username FROM users WHERE username=?", request.form.get("username"))):
            message1 = "Username already taken"
            return render_template("register.html", message1=message1)

        elif (not request.form.get("confirmation")) or (request.form.get("confirmation") != request.form.get("password")):
            message1 = "Confirmation invalid"
            return render_template("register.html", message1=message1)

        else:
            hash = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hash)
            return redirect("/login")

    else:
        return render_template("register.html", message1=message1)


@app.route("/passwordchange", methods=["GET", "POST"])
@login_required
def passwordchange():
    message_success = None
    message_alert = None
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Change unsuccessful
        if not request.form.get("username"):
            message_alert = "Must provide username"
            return render_template("passwordchange.html", message_success=message_success, message_alert=message_alert)

        elif not request.form.get("old_password"):
            message_alert = "Must provide password"
            return render_template("passwordchange.html", message_success=message_success, message_alert=message_alert)

        elif (not request.form.get("confirmation")) or ((request.form.get("confirmation")) != (request.form.get("new_password"))):
            message_alert = "Confirmation invalid"
            return render_template("passwordchange.html", message_success=message_success, message_alert=message_alert)

        elif len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            message_alert = "Invalid username and/or password"
            return render_template("passwordchange.html", message_success=message_success, message_alert=message_alert)

        # Change successful
        else:
            new_hash = generate_password_hash(request.form.get("new_password"))
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, session["user_id"])
            message_success = "Password is changed successfully"
            return render_template("passwordchange.html", message_success=message_success, message_alert=message_alert)
    else:
        return render_template("passwordchange.html", message_success=message_success, message_alert=message_alert)


# For the about us page
@app.route("/aboutus", methods=["GET"])
@login_required
def aboutus():
    return render_template("aboutus.html")
