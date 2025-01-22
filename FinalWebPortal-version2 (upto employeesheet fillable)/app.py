from flask import Flask, request, redirect, render_template, flash, url_for
import pyodbc
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# SQL Server connection settings
server = 'JG-07\\MSSQLSERVER2022'
database = 'WEBPORTAL'
connection_string = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

# Password hashing utility
ph = PasswordHasher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        emp_w_id = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = ph.hash(password)

        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()

                # Check for duplicate W#
                cursor.execute("SELECT COUNT(*) FROM EMP_USER WHERE Emp_W_Id = ?", emp_w_id)
                if cursor.fetchone()[0] > 0:
                    flash("W# already registered. Please log in.")
                    return redirect(url_for('register'))

                # Insert user into EMP_USER table
                cursor.execute(
                    "INSERT INTO EMP_USER (Emp_W_Id, Emp_Pswd_hash) VALUES (?, ?)",
                    emp_w_id, hashed_password
                )
                conn.commit()

                flash("Registration successful! You can now log in.")
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred during registration. Please try again.")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    emp_w_id = request.form['email']
    password = request.form['password']
    login_time = datetime.datetime.now()

    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()

            # Verify user credentials
            cursor.execute("SELECT Emp_Pswd_hash FROM EMP_USER WHERE Emp_W_Id = ?", emp_w_id)
            row = cursor.fetchone()
            if row:
                stored_hash = row[0]
                try:
                    ph.verify(stored_hash, password)

                    # Log successful login time
                    cursor.execute("INSERT INTO LOGIN_LOGS (Emp_W_Id, Login_Time) VALUES (?, ?)", emp_w_id, login_time)
                    conn.commit()

                    return redirect(url_for('dashboard'))
                except VerifyMismatchError:
                    flash("Incorrect password.")
                    return redirect(url_for('index'))
            else:
                flash("Invalid user or W#.")
                return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while processing your request.")
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/employeeTimesheet')
def employee_timesheet():
    return render_template('employeeTimeSheet.html')


if __name__ == '__main__':
    app.run(debug=True)
