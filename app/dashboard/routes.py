from flask import Blueprint, render_template, redirect, url_for
from .models import Dashboard
from app import db

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard.route("/<int:id>", methods=['GET'])
def user_dashboard(id):
    # user_id null dönüyor bağlantı kurulamadı parent ve child muhabbetine 
    my_dashboard = Dashboard.query.filter(Dashboard.user_id==id).first()
    return my_dashboard


@dashboard.route("/")
def remove_word(id):
    return "dashboard"
