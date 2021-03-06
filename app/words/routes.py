from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from .forms import SearchForm
from app.models.models import Dashboard
from sqlalchemy.orm.attributes import flag_modified
from app import db
from app.config import RAPID_API_HOST, RAPID_API_KEY
import requests
import json
from app.loginreq import login_required

words = Blueprint("words", __name__)


BASE_URL = "https://wordsapiv1.p.rapidapi.com/words/"

headers = {
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": RAPID_API_HOST,
}


@words.route("/", methods=["GET", "POST"])
@login_required
def search_word():
    form = SearchForm()
    if request.method == "POST":
        dashboard = Dashboard.query.filter_by(user_id=session["user_id"]).first()
        form = SearchForm()
        searchedWord = form.search.data

        def_url = BASE_URL + searchedWord + "/definitions"
        def_r = requests.get(def_url, headers=headers)
        def_result = def_r.json()

        fq_url = BASE_URL + searchedWord + "/frequency"
        fq_r = requests.get(fq_url, headers=headers)
        fq_result = fq_r.json()

        meanings = []
        try:
            for meaning in def_result["definitions"]:
                meanings.append(meaning["definition"])
        except:
            flash('This word is does not exist')
            return render_template('index.html', form=form)

        session["search_data"] = def_result
        session["frequency_data"] = fq_result["frequency"]["perMillion"]
        
        if dashboard:
            # Adds 1 point to search tracker value,
            for i in dashboard.wordlist["words"]:
                if i["word"] == def_result["word"]:
                    i["searched"] += 1
                    flag_modified(dashboard, "wordlist")
                    db.session.commit()
                    return render_template("index.html",meanings=meanings,form=form,word=searchedWord)
        
        return render_template("index.html", meanings=meanings, form=form, word=searchedWord) 
    return render_template("index.html", form=form)


@words.route("/save", methods=["GET", "POST"])
def save_word():
    if request.method == "POST":
        dashboard = Dashboard.query.filter_by(user_id=session["user_id"]).first()
        data = session["search_data"]
        word = data["word"]
        meaning = data["definitions"][0]["definition"]
        permillion = session["frequency_data"]
        if dashboard:
            for i in dashboard.wordlist["words"]:
                if i["word"] == data["word"]:
                    flash("This word is already saved!", "Danger")
                    return redirect(url_for("words.search_word"))

            word_details = {
                "word": word,
                "definition": meaning,
                "power": 0,
                "points":0,
                "searched": 0,
                "asked": 0,
                "permillion": permillion
            }

            w = dashboard.wordlist["words"]
            w.append(word_details)
            dashboard.wordlist["words"] = w
            flag_modified(dashboard, "wordlist")
            db.session.commit()
            formula(session["user_id"], word)
            flash("Word is saved to your dashboard", "Success")
            return redirect(url_for("words.search_word"))

        else:
            word_details = [
                {
                    "word": word,
                    "definition": meaning,
                    "power": 0,
                    "points":0,
                    "searched": 0,
                    "asked": 0,
                    "permillion": permillion
                }
            ]
            word_info = {"words": word_details}
            newDashboard = Dashboard(user_id=session["user_id"], wordlist=word_info)
            db.session.add(newDashboard)
            db.session.commit()
            formula(session["user_id"], word)
            flash("Word is saved to your dashboard", "Success")
            return redirect(url_for("words.search_word"))


def formula(user_id, word):
    dashboard = Dashboard.query.filter_by(user_id=user_id).first()
    for i in dashboard.wordlist["words"]:
        if i["word"] == word:
            points = i["points"]
            permillion = i["permillion"]
            searched = i["searched"]
            asked = i["asked"]


    power_index_i = 0.27 * 10000 // permillion
    power_index_f = 0.27 * 10000 / permillion

    if permillion < 1:
        power = 100
    elif 100 > permillion >= 1:
        power = 85
    elif 500 > permillion >= 100:
        power = 60
    elif 1000 > permillion >= 500:
        power = 50
    elif 5000 > permillion >= 1000:
        power = 40
    elif 10000 > permillion >= 5000:
        power = 30
    else:
        power = 15

    # Points
    if -20 <= points <= -10:
        power += 6
    if -10 < points <= 0:
        power += 3
    elif 20 >= points > 0:
        power -= 3
    elif 50 >= points > 20:
        power -= 6
    elif points > 50:
        power -= 12

    # Searched
    if searched == 0:
        pass
    elif 5 >= searched > 0:
        power -= 3
    elif searched > 5:
        power -= 8

    # Asked
    if asked == 0:
        pass
    elif 3 >= asked > 0:
        power -= 3
    elif asked > 3:
        power -= 6

    # To avoid the power attribute to go sub zero
    if power < 0:
        power = 0

    for i in dashboard.wordlist["words"]:
        if i["word"] == word:
            i["power"] = power
            flag_modified(dashboard, "wordlist")
            db.session.commit()
