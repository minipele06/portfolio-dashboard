import csv
import pandas as pd 
import os

def login_auth(username,password):
    csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "credentials", "u&p.csv")
    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Username"] == str(username):
                if row["Password"] == str(password):
                    result = "Logged In"
                    return result
                    exit()

    result = "Username/Password Incorrect"
    return result
