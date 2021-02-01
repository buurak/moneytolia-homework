from flask import Blueprint, render_template, redirect, url_for, session
from app.models.models import Dashboard
from app import db
import json

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


@dashboard.route("/")
def remove_word(id):
    return "dashboard"
