import csv
import os

def signup(email,username,password):
    csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "credentials", "u&p.csv")
    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Username"] == str(username):
                result = "Username Is Already Taken"
                return result
            elif row["Email"] == str(email):
                result = "Already Account Associated With That Email"
                return result

    with open(csv_filepath, "a+",newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Username", "Password", "Email"])
        writer.writerow({"Username": username, "Password": password, "Email": email})
        result = "Registration Complete, Please Use Login Window"
        return result
