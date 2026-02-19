import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


def clean_name(name):
    return name.strip()


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition_name = clean_name(request.form.get("competition", ""))
    club_name = clean_name(request.form.get("club", ""))
    places_raw = clean_name(request.form.get("places", ""))

    foundClub = next((c for c in clubs if c["name"] == club_name), None)
    foundCompetition = next(
        (c for c in competitions if c["name"] == competition_name), None
    )

    if not foundClub or not foundCompetition:
        flash("Club ou competition not found.")
        return redirect(url_for("index"))

    try:
        placesRequired = int(places_raw)
    except ValueError:
        flash("Please enter a valid number of places ")
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )

    if placesRequired <= 0:
        flash("you must purchase at least 1 place ")
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )

    if placesRequired > 12:
        flash("You cannot purchase more than 12 places per competition.")
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )

    placesAvailable = int(foundCompetition.get("numberOfPlaces", 0))
    if placesAvailable <= 0:
        flash("Sorry, this competition is full.")
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )

    if placesRequired > placesAvailable:
        flash(f"Only {placesAvailable} places remaining.")
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )

    clubPoints = int(foundClub.get("points", 0))
    if placesRequired > clubPoints:
        flash("You do not have enough points to purchase these places.")
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )

    foundCompetition["numberOfPlaces"] = str(placesAvailable - placesRequired)
    foundClub["points"] = str(clubPoints - placesRequired)

    flash(f"Great-booking complete! You purchased {placesRequired} place(s).")
    return render_template("welcome.html", club=foundClub, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
