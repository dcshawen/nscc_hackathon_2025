import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize Flask app
app = Flask(__name__)
app.secretKey = "ctrlAltDefeat"

# Initialize PasswordHasher
ph = PasswordHasher()

# Database connection
def getDbConnection():
    try:
        connection = pyodbc.connect(
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=JG-07\MSSQLSERVER2022;"  # Replace with your server name
            r"DATABASE=TSDB;"            # Replace with your database name
            r"Trusted_Connection=yes;"
        )
        return connection
    except Exception as error:
        print(f"Database connection failed: {error}")
        return None

# Insert user into the database
def insertUser(userName, passwordHash):
    try:
        connection = getDbConnection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO EMP_USER (Emp_W_Id, Emp_Pswd_hash) VALUES (?, ?)",
                userName, passwordHash
            )
            connection.commit()
        return True
    except Exception:
        return False

# Fetch user from the database
def fetchUser(userName):
    try:
        connection = getDbConnection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT Emp_W_Id, portal_type FROM EMP_USER WHERE Emp_W_Id = ?",
                userName
            )
            return cursor.fetchone()
    except Exception:
        return None

# Password hashing functions
def hashPassword(password):
    return ph.hash(password)

def verifyPassword(storedHash, password):
    try:
        return ph.verify(storedHash, password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False

# Routes
@app.route("/")
def home():
    return "<h1>Welcome to the Flask Authentication App</h1>"

@app.route("flask_auth_app\\templates\\register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        userName = request.form["username"]
        password = request.form["password"]
        hashedPassword = hashPassword(password)

        if insertUser(userName, hashedPassword):
            flash("Registration successful!", "success")
            return redirect(url_for("login"))
        else:
            flash("Username already exists.", "warning")
    return render_template("register.html")

@app.route("flask_auth_app\\templates\\login.html", methods=["GET", "POST"])
def login():
    """Handles user login dynamically."""
    if request.method == "POST":
        userName = request.form["username"]
        password = request.form["password"]
        userRecord = fetchUser(userName)

        if userRecord:
            storedHash, portalType = userRecord
            if verifyPassword(storedHash, password):
                # Password is valid; redirect to the appropriate portal
                return redirect(url_for("portal", portalType=portalType))
            else:
                flash("Invalid password. Please try again.", "danger")
        else:
            flash("User not found. Please check your username.", "warning")

    return render_template("login.html")

@app.route("/portal/<portalType>")
def portal(portalType):
    #Displays the appropriate portal page based on user credentials
    validPortals = ["portal1", "portal2", "portal3"]
    if portalType in validPortals:
        return render_template(f"{portalType}.html", portal=portalType)
    else:
        return "Invalid portal."

if __name__ == "__main__":
    app.run(debug=True)
