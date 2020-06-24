from flask import Blueprint, render_template, redirect, request, flash
from dotenv import load_dotenv
import csv
import os

from app import Log_status
from app.login import login_auth
from app.signup import signup
from app.active_user import active_user
from app.login import create_folder

Log_stat = "out"
home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    return render_template("home.html")

@home_routes.route("/about")
def about():
    return render_template("about.html")

@home_routes.route("/allocations")
def alloc():
    return render_template("allocations.html")

@home_routes.route("/watch-list")
def watch():
    return render_template("watch_list.html")

@home_routes.route("/register")
def register():
    return render_template("new_user_form.html")

@home_routes.route("/dashboard", methods=["GET"])
def dashboard():
    results = active_user()
    return render_template("dashboard.html", username=results)

@home_routes.route("/users/login", methods=["POST"])
def check_user():
    print("FORM DATA:", dict(request.form))
    user = dict(request.form)
    # FYI: "warning", "primary", "danger", "success", etc. are bootstrap color classes
    # ... see https://getbootstrap.com/docs/4.3/components/alerts/
    # ... and the flash messaging section of the "bootstrap_layout.html" file for more details
    results = login_auth(user['username'],user['password'])
    if str(results) == "Username/Password Incorrect":
        flash(f"{results}", "danger")
        return redirect("/")
    else:
        create_folder(user['username'])
        csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{user['username']}", f"{user['username']}.csv")
        with open(csv_file_path, "r") as csv_file: # "r" means "open the file for reading"
            reader = csv.DictReader(csv_file) # assuming your CSV has headers
        flash(f"{results}, {csv_file_path}", "success")
        return render_template("dashboard.html", username=user['username'], results=reader)

@home_routes.route("/users/create", methods=["POST"])
def create_user():
    print("FORM DATA:", dict(request.form))
    user = dict(request.form)
    # FYI: "warning", "primary", "danger", "success", etc. are bootstrap color classes
    # ... see https://getbootstrap.com/docs/4.3/components/alerts/
    # ... and the flash messaging section of the "bootstrap_layout.html" file for more details
    results = signup(user['email'],user['username'],user['password'])
    flash(f"{results}", "success")
    return redirect("/")

@home_routes.route("/logout")
def logout():
    flash(f"You Have Succesfully Logged Out", "success")
    return redirect("/")
