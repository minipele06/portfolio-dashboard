import csv
import os

def active_user():
    csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "users", "active_user.csv")
    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Username"] != "Username":
                result = row["Username"]
                return result
                exit()