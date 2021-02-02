from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from sqlalchemy.orm.attributes import flag_modified
from app.models.models import Dashboard
from app import db
import json
import random

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard.route("/", methods=['GET'])
def user_dashboard():
    my_dashboard = Dashboard.query.filter(Dashboard.user_id==session['user_id']).first()
    my_words = []
    for word in my_dashboard.wordlist['words']:
        my_words.append(word['word'])
        
    if len(my_words)>10:
        print("10dan büyük")
        
    return render_template('dashboard.html', my_words=my_words)


@dashboard.route("/quiz/", methods=['GET','POST'])
def start_quiz():
    my_dashboard = Dashboard.query.filter(Dashboard.user_id==session['user_id']).first()
    word_pool = []
    for word in my_dashboard.wordlist['words']:
        word_pool.append(word['word'])
    correct_word = random.choice(word_pool)
    for i in my_dashboard.wordlist['words']:
        if i['word']==correct_word:
            correct_definition = i['definition']
    word_pool.remove(correct_word)
    incorrect_options = random.sample(word_pool, 2)
    word1, word2 = incorrect_options
    question_list = [
        word1,
        word2,
        correct_word
    ]
    random.shuffle(question_list)
    session['correct_word']=correct_word
    for j in my_dashboard.wordlist['words']:
        if j['word'] == correct_word:
            for k in my_dashboard.wordlist['words']:
                if k['word']== correct_word:
                    k['asked']+=1
                    flag_modified(my_dashboard, "wordlist")
                    db.session.commit()
                    return render_template('dashboard.html',start='start',correct_definition=correct_definition, question_list=question_list)

@dashboard.route("/check", methods=['POST'])
def check():
    my_dashboard = Dashboard.query.filter(Dashboard.user_id==session['user_id']).first()
    answer = request.form['option']
    if answer == session['correct_word']:
        my_dashboard.points+=1
        flag_modified(my_dashboard, "points")
        db.session.commit()   
    else:
        my_dashboard.points-=1
        flag_modified(my_dashboard, "points")
        db.session.commit()
        flash('Wrong answer','danger')

    return redirect(url_for('dashboard.start_quiz'))