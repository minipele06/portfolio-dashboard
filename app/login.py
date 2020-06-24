import csv
import os

def login_auth(username,password):
    csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "credentials", "u&p.csv")
    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Username"] == str(username):
                if row["Password"] == str(password):
                    csv_filepath2 = os.path.join((os.path.dirname(__file__)),"..", "users", "active_user.csv")
                    with open(csv_filepath2, "w") as csv_file: # "w" means "open the file for writing"
                        writer = csv.DictWriter(csv_file, fieldnames=["Username", "Email"])
                        writer.writeheader() # uses fieldnames set above
                        writer.writerow({"Username": username, "Email": row["Email"]})
                    result = "Logged In"
                    return result

    result = "Username/Password Incorrect"
    return result
