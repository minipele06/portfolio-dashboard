from flask import Blueprint, render_template, redirect, request, flash
from dotenv import load_dotenv
import csv
import os
import pandas as pd 

from app.login import login_auth
from app.signup import signup
from app.active_user import active_user
from app.login import create_folder

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    return render_template("home.html")

@home_routes.route("/about")
def about():
    return render_template("about.html")

@home_routes.route("/buy-sell")
def buy_sell():
    return render_template("buy_sell.html")

@home_routes.route("/transactions")
def transac():
    username = active_user()
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}_transactions.csv")
    results = pd.read_csv(csv_file_path).to_dict("records")
    return render_template("transactions.html", results=results)

@home_routes.route("/register")
def register():
    return render_template("new_user_form.html")

@home_routes.route("/dashboard", methods=["GET"])
def dashboard():
    username = active_user()
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}.csv")
    csv_file_path2 = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}_transactions.csv")
    results = pd.read_csv(csv_file_path).to_dict("records")
    stocks_df = pd.read_csv(csv_file_path)
    transactions_df = pd.read_csv(csv_file_path2)
    cash_value = transactions_df["Value"].sum()
    positions = stocks_df["Total Value"].sum()
    total = cash_value + positions
    return render_template("dashboard.html", username=username, results=results, value=cash_value, value2=positions, value3=total)

@home_routes.route("/users/login", methods=["POST"])
def check_user():
    user = dict(request.form)
    username = user['username']
    password = user['password']
    # FYI: "warning", "primary", "danger", "success", etc. are bootstrap color classes
    login_status = login_auth(username,password)
    if str(login_status) == "Username/Password Incorrect":
        flash(f"{login_status}", "danger")
        return redirect("/")
    else:
        create_folder(username)
        flash(f"{login_status}", "success")
        return redirect("/dashboard")

@home_routes.route("/users/create", methods=["POST"])
def create_user():
    print("FORM DATA:", dict(request.form))
    user = dict(request.form)
    results = signup(user['email'],user['username'],user['password'])
    if str(results) == "Username Is Already Taken":
        flash(f"{results}", "danger")
    else:
        flash(f"{results}", "success")
    return redirect("/")

@home_routes.route("/users/buy", methods=["POST"])
def buy_order():
    print("FORM DATA:", dict(request.form))
    user = dict(request.form)
    flash(f"{user}", "success")
    return redirect("/buy-sell")

@home_routes.route("/users/sell", methods=["POST"])
def sell_order():
    print("FORM DATA:", dict(request.form))
    user = dict(request.form)
    flash(f"{user}", "success")
    return redirect("/buy-sell")

@home_routes.route("/logout")
def logout():
    flash(f"You Have Succesfully Logged Out", "success")
    return redirect("/")
