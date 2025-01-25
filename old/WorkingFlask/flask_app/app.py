import os
from flask import Flask, render_template, request, redirect, url_for, flash
from argon2 import PasswordHasher
import pyodbc

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "ctrlAltDefeat"

# Initialize PasswordHasher
ph = PasswordHasher() 

# Database connection
def getDbConnection():
    try:
        connection = pyodbc.connect(
            r"DRIVER={ODBC Driver 18 for SQL Server};"
            r"SERVER=PEEPHONE;"  # Replace with your server name
            r"DATABASE=EMPTIMESHEET;"  # Replace with your database name
            r"Trusted_Connection=yes;"
            r"TrustServerCertificate=yes;"
        )
        print("Database connection successful")
        return connection
    except Exception as error:
        print(f"Database connection failed: {error}")
        return None

# Insert user into the database
def insertUser(userName, passwordHash, portalType=1):
    try:
        connection = getDbConnection()
        if connection is None:
            raise Exception("Failed to connect to the database")
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO EMP_USER (Emp_W_Id, Emp_Pswd_hash, Emp_Portal) VALUES (?, ?, ?)",
                userName, passwordHash, portalType
            )
            connection.commit()
        print("User inserted successfully")
        return True
    except Exception as error:
        print(f"Failed to insert user: {error}")
        return False

# Fetch user from the database
def fetchUser(userName):
    try:
        connection = getDbConnection()
        if connection is None:
            raise Exception("Failed to connect to the database")
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT Emp_Pswd_hash, Portal_Type FROM EMP_USER WHERE Emp_W_Id = ?",
                userName
            )
            result = cursor.fetchone()
            print(f"Fetched user: {result}")
            return result
    except Exception as error:
        print(f"Failed to fetch user: {error}")
        return None

# Verify password
def verifyPassword(storedHash, password):
    try:
        ph.verify(storedHash, password)
        return True
    except:
        return False
    
# @app.route("/")
# def home():
#     return render_template("/index.html")

@app.route("/", methods=["GET", "POST"])
def login():
    """Handles user login and registration dynamically."""
    if request.method == "POST":
        userName = request.form["email"]
        password = request.form["password"]
        userRecord = fetchUser(userName)

        if userRecord:
            storedHash, portalType = userRecord
            try:
                verifyPassword(storedHash, password)
                # Password is valid; redirect to the appropriate portal
                if portalType == 1:
                    return redirect(url_for("portal", portalType="employeeTimeSheet"))
                elif portalType == 2:
                    return redirect(url_for("portal", portalType="supervisorTimeSheet"))
                elif portalType == 3:
                    return redirect(url_for("portal", portalType="adminTimeSheet1"))
            except:
                flash("Invalid password. Please try again.", "danger")
        else:
            # User not found, register the user
            hashedPassword = ph.hash(password)
            try: 
                insertUser(userName, hashedPassword)
                flash("Registration successful! Redirecting to employee timesheet.", "success")
                return redirect(url_for("portal", portalType="employeeTimeSheet"))
            except:
                flash("Failed to register user. Please try again.", "danger")

    return render_template("/index.html")

@app.route("/<portalType>")
def portal(portalType):
    """Displays the appropriate portal page based on user credentials."""
    validPortals = ["employeeTimeSheet", "supervisorTimeSheet", "adminTimeSheet1"]
    if portalType in validPortals:
        return render_template(f"/{portalType}.html", portal=portalType)
    else:
        return "Invalid portal."

if __name__ == "__main__":
    app.run(debug=True)
