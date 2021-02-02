from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from .forms import SearchForm
from app.models.models import Dashboard
from sqlalchemy.orm.attributes import flag_modified
from app import db
import requests
import json

words = Blueprint("words", __name__)


BASE_URL = "https://wordsapiv1.p.rapidapi.com/words/"
headers = {
    "x-rapidapi-key": "821b950c45msh91f67e1bf3b5100p198b0djsnfe5b8481ac28",
    "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
}


@words.route("/search", methods=["GET", "POST"])
def search_word():
    form = SearchForm()
    if request.method == "POST":
        dashboard = Dashboard.query.filter_by(user_id=session["user_id"]).first()
        form = SearchForm()
        searchedWord = form.search.data
        url = BASE_URL + searchedWord + "/definitions"
        r = requests.get(url, headers=headers)
        result = r.json()
        meanings = []
        for meaning in result["definitions"]:
            meanings.append(meaning["definition"])
        session["word"] = searchedWord
        session["data"] = result
        if dashboard:
            #Adds 1 point to search tracker value, 
            for i in dashboard.wordlist['words']:
                if i['word']==result['word']:
                    for j in dashboard.wordlist['words']:
                        if j['word']==i['word']:
                            j['searched']+=1
                            flag_modified(dashboard, "wordlist")
                            db.session.commit()
                            return render_template("index.html", meanings=meanings, form=form, word=searchedWord)
        return render_template("index.html", meanings=meanings, form=form, word=searchedWord)

    return render_template("index.html", form=form)


@words.route("/save", methods=["GET", "POST"])
def save_word():
    if request.method == "POST":
        dashboard = Dashboard.query.filter_by(user_id=session["user_id"]).first()
        data = session["data"]
        word = data["word"]
        meaning = data["definitions"][0]["definition"]

        if dashboard:
            for i in dashboard.wordlist["words"]:
                if i["word"] == data["word"]:
                    flash("This word is already saved!")
                    return redirect(url_for("words.search_word"))

            word_details = {
                "word": word,
                "definition": meaning,
                "power": 10,
                "searched": 0,
                "asked": 0,
                "is_asked":False
            }

            w = dashboard.wordlist["words"]
            w.append(word_details)
            dashboard.wordlist["words"] = w
            flag_modified(dashboard, "wordlist")
            db.session.commit()
            return redirect(url_for("words.search_word"))

        else:
            word_details = [
                {
                    "word": word,
                    "definition": meaning,
                    "power": 10,
                    "searched": 0,
                    "asked": 0,
                    "is_asked":False
                }
            ]
            word_info = {"words": word_details}
            newDashboard = Dashboard(user_id=session["user_id"], wordlist=word_info)
            db.session.add(newDashboard)
            db.session.commit()
            return redirect(url_for("words.search_word"))
