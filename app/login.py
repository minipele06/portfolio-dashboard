import csv
import pandas as pd 
import os

def row_count(filename):
    with open(filename) as in_file:
        return sum(1 for _ in in_file)

username = input("Please Enter Your Username: ")
password = input("Please Enter Your Password: ")

csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "credentials", "u&p.csv")

with open(csv_filepath, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row["Username"] == str(username):
            if row["Password"] == str(password):
                print("Logged In")
                exit()

print("Username/Password Incorrect")