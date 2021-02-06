from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from .forms import RegisterForm, LoginForm
from app.models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.loginreq import login_required

user = Blueprint("user", __name__)


@user.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user is not None and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for("words.search_word"))
        else:
            flash('Username or Password Incorrect', "Danger")
            return redirect(url_for('user.login'))
    return render_template('login.html',form=form)

@user.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate and request.method == "POST":
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for("user.login"))
        else:
            newUser = User(username=username, password=generate_password_hash(password))
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for("user.login"))
    elif request.method == 'GET':
        return render_template("register.html", form=form)

@user.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('user.login'))