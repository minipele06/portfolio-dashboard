from flask import Blueprint, render_template, redirect, request, flash
from dotenv import load_dotenv
import csv
import os
import pandas as pd 

#loading functions from python scripts
from app.login import login_auth
from app.signup import signup
from app.active_user import active_user
from app.active_user import clear_user
from app.login import create_folder
from app.live_price import live_price
from app.live_price import transac_rec
from app.live_price import update_prices
from app.live_price import buy_transac
from app.live_price import sell_transac
from app.format import format_dict
from app.format import format_dict2

#format to USD with two decimals
def to_usd(my_price):
    return f"${my_price:,.2f}"

#load API_KEY from .env
load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

#map home routes
home_routes = Blueprint("home_routes", __name__)

#Home page with function to clear user from active_user.csv
@home_routes.route("/")
def index():
    clear_user()
    return render_template("home.html")

#About page with render template
@home_routes.route("/about")
def about():
    return render_template("about.html")

#Trading page with render template
@home_routes.route("/buy-sell")
def buy_sell():
    return render_template("buy_sell.html")

#Transaction History page with render template that pulls info from transaction.csv on every visit
@home_routes.route("/transactions")
def transac():
    username = active_user()
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}_transactions.csv")
    results = pd.read_csv(csv_file_path).to_dict("records")
    format_dict2(results)
    return render_template("transactions.html", results=results)

#Dashboard page with render template that pulls info from user csv on each visit and calculates account values
@home_routes.route("/dashboard", methods=["GET"])
def dashboard():
    username = active_user()
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}.csv")
    csv_file_path2 = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}_transactions.csv")
    results = pd.read_csv(csv_file_path).to_dict("records")
    if len(results) == 0:
        results = ""
    stocks_df = pd.read_csv(csv_file_path)
    transactions_df = pd.read_csv(csv_file_path2)
    cash_value = float(transactions_df["Value"].sum())
    positions = stocks_df["Total Value"].sum()
    if positions == " ":
        positions = 0.00
        total = cash_value
    else:
        format_dict(results)
        positions = float(positions)
        total = cash_value + positions
    return render_template("dashboard.html", username=username, results=results, value=to_usd(cash_value), value2=to_usd(positions), value3=to_usd(total))

#User login request where successful authentication leads user to user-specific dashboard page
@home_routes.route("/users/login", methods=["POST"])
def check_user():
    user = dict(request.form)
    if user['username'] == "" or user['password'] == "":
        flash(f"Invalid Entry", "danger")
        return redirect("/")
    else:
        username = user['username']
        password = user['password']
        login_status = login_auth(username,password)
        if str(login_status) == "Username/Password Incorrect":
            flash(f"{login_status}", "danger")
            return redirect("/")
        else:
            create_folder(username)
            flash(f"{login_status}", "success")
            return redirect("/dashboard")

#User registration that checks user details and successful registration is added to username and password file
@home_routes.route("/users/create", methods=["POST"])
def create_user():
    user = dict(request.form)
    if user['email'] == "" or user['username'] == "" or user['password'] == "":
        flash(f"Invalid Entry", "danger")
    elif not "@" in user['email'] or not "." in user['email']:
        flash(f"Invalid Email", "danger")
    else:
        results = signup(user['email'],user['username'],user['password'])
        if str(results) == "Username Is Already Taken" or str(results) == "Already Account Associated With That Email":
            flash(f"{results}", "danger")
        else:
            flash(f"{results}", "success")
    return redirect("/")

#User purchase is checked for validity and posted to user csv and transaction csv
@home_routes.route("/users/buy", methods=["POST"])
def buy_order():
    user = dict(request.form)
    username = active_user()
    results = live_price(user['ticker'],API_KEY)
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}.csv")
    pos_count = len(pd.read_csv(csv_file_path).to_dict("records"))
    csv_file_path2 = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}_transactions.csv")
    data = pd.read_csv(csv_file_path).to_dict("records")
    transactions_df = pd.read_csv(csv_file_path2)
    cash_value = float(transactions_df["Value"].sum())
    stock = [n["Stock"] for n in data if n["Stock"] == user['ticker']]
    if str(results) == "Invalid Stock Symbol, Try Again":
        flash(f"{results}", "danger")
    elif len(stock) > 0:
        shares = int(user['share_count'])
        if (shares*results) > cash_value:
            flash(f"Insufficient Funds", "danger")
        else:
            buy_transac(csv_file_path,stock,shares,results)
            flash(f"You Bought {shares} Shares of {user['ticker']} For {to_usd(results*shares)}", "success")
            transac_rec(user['ticker'],results,shares,username,"Buy+")
    elif pos_count > 4:
        flash(f"Reached Positions Limit of 5, Please Sell Position Before Buying A New One", "danger")
    else:
        shares = int(user['share_count'])
        if (shares*results) > cash_value:
            flash(f"Insufficient Funds", "danger")
        else:   
            flash(f"You Bought {shares} Shares of {user['ticker']} For {to_usd(results*shares)}", "success")
            transac_rec(user['ticker'],results,shares,username,"Buy")
    return redirect("/buy-sell")

#User sale is checked for validity and posted to user csv and transaction csv
@home_routes.route("/users/sell", methods=["POST"])
def sell_order():
    username = active_user()
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}.csv")
    data = pd.read_csv(csv_file_path).to_dict("records")
    user = dict(request.form)
    stock = [n["Stock"] for n in data if n["Stock"] == user['ticker']]
    shares_aval = [n["Shares"] for n in data if n["Stock"] == user['ticker']]
    if not stock:
        flash(f"You Do Not Own That Stock", "danger")
    elif int(user['share_count']) > shares_aval[0]:
        flash(f"You Do Not Own That Many Shares", "danger")
    else:
        results = live_price(user['ticker'],API_KEY)
        if str(results) == "Invalid Stock Symbol, Try Again":
            flash(f"{results}", "danger")
        else:
            shares = int(user['share_count'])
            sell_transac(csv_file_path,stock,shares,results,shares_aval[0])
            transac_rec(user['ticker'],results,shares,username,"Sell")
            flash(f"You Sold {shares} Shares of {user['ticker']} For {to_usd(results*shares)}", "success")
    return redirect("/buy-sell")

#Update dashboard with live prices and recalculate stock values and unrealized gain/loss
@home_routes.route("/users/update")
def update():
    username = active_user()
    update_prices(username,API_KEY)
    flash(f"Market Values Updated", "success")
    return redirect("/dashboard")

#Forgot Password flashes warning
@home_routes.route("/forgot-password")
def forgot():
    flash(f"You Forgot Your Password", "warning")
    return redirect("/")

#User logout clears user from active_user.csv and brings user back to home page
@home_routes.route("/logout")
def logout():
    flash(f"You Have Succesfully Logged Out", "success")
    clear_user()
    return redirect("/")
