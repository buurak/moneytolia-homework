from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from .forms import SearchForm
from app.dashboard.models import Dashboard
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
        return render_template(
            "index.html", meanings=meanings, form=form, word=searchedWord
        )

    return render_template("index.html", form=form)


@words.route("/save", methods=["GET", "POST"])
def save_word():
    if request.method == "POST":
        dashboard = Dashboard.query.filter_by(user_id=session["user_id"]).first()
        data = session["data"]
        word = data["word"]
        meanings = []
        for meaning in data["definitions"]:
            meanings.append(meaning["definition"])

        if dashboard:
            for i in dashboard.wordlist['words']:
                print(i['word'], data['word'])
                if i['word'] == data['word']:
                    print("if e girdi")
                    flash('This word is already saved!')
                    return redirect(url_for('words.search_word'))
                
            print("else durumu")
            word_details = {
                "word": word, 
                "definitions": meanings, 
                "point": 4
                }

            w = dashboard.wordlist["words"]
            w.append(word_details)
            dashboard.wordlist['words'] = w
            flag_modified(dashboard, 'wordlist')
            db.session.commit()
            return redirect(url_for("words.search_word"))

        else:
            print("dashboard yok")
            word_details = [{
                "word": word, 
                "definitions": meanings, 
                "point": 4
            }]

            word_info = {"words": word_details}
            newDashboard = Dashboard(
                user_id=session["user_id"], wordlist=word_info
            )
            db.session.add(newDashboard)
            db.session.commit()
            return redirect(url_for("words.search_word"))
