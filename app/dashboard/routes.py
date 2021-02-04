from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from sqlalchemy.orm.attributes import flag_modified
from app.models.models import Dashboard
from app.words.routes import formula
from app import db
import json
import random

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard.route("/", methods=["GET"])
def user_dashboard():
    my_dashboard = Dashboard.query.filter(Dashboard.user_id == session["user_id"]).first()
    count=0
    if my_dashboard:
        my_words = []
        for word in my_dashboard.wordlist["words"]:
            info = {"word": word["word"], "power": word["power"]}
            my_words.append(info)
        for word in my_words:
            formula(session["user_id"], word["word"])
        count = len(my_words)
        return render_template("dashboard.html", my_words=my_words, count=count)
    return render_template("dashboard.html",count=count)

@dashboard.route("/quiz/", methods=["GET", "POST"])
def start_quiz():
    my_dashboard = Dashboard.query.filter(Dashboard.user_id == session["user_id"]).first()
    word_pool = []
    for word in my_dashboard.wordlist["words"]:
        word_pool.append(word["word"])
    correct_word = random.choice(word_pool)
    for i in my_dashboard.wordlist["words"]:
        if i["word"] == correct_word:
            correct_definition = i["definition"]
    word_pool.remove(correct_word)
    incorrect_options = random.sample(word_pool, 2)
    word1, word2 = incorrect_options
    question_list = [word1, word2, correct_word]
    random.shuffle(question_list)
    session["correct_word"] = correct_word
    session["incorrect_words"] = incorrect_options
    for j in my_dashboard.wordlist["words"]:
        if j["word"] == correct_word:
            j["asked"] += 1
            flag_modified(my_dashboard, "wordlist")
            db.session.commit()
            return render_template("quiz.html",start="start",correct_definition=correct_definition,question_list=question_list,)


@dashboard.route("/check", methods=["POST"])
def check():
    my_dashboard = Dashboard.query.filter(Dashboard.user_id == session["user_id"]).first()
    answer = request.form["option"]
    word1 = session["incorrect_words"][0]
    word2 = session["incorrect_words"][1]
    if answer == session["correct_word"]:
        for k in my_dashboard.wordlist["words"]:
            if k["word"] == answer:
                k["points"] += 1
                flag_modified(my_dashboard, "wordlist")
                db.session.commit()
    else:
        for i in my_dashboard.wordlist['words']:
            if i['word'] == answer:
                i['points']-=2
        for i in my_dashboard.wordlist['words']:
            if i['word'] == word1:
                i['points']-=1
        for i in my_dashboard.wordlist['words']:
            if i['word'] == word2:
                i['points']-=1
        flag_modified(my_dashboard,"wordlist")
        db.session.commit()
        flash("Wrong answer", "danger")
    return redirect(url_for("dashboard.start_quiz"))
