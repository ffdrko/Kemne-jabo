from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'database'
app.config['MYSQL_DB'] = 'kemne_jabo'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    details = request.form
    msg = ""
    if request.method == "POST" and 'Email' in details and 'First Name' in details and 'Last Name' in details and 'Mobile' in details and 'House' in details and 'Street' in details and 'Thana' in details and 'District' in details and 'Postal Code' in details and 'Password' in details and 'Confirm' in details and 'Question' in details and 'Answer' in details and 'Hint' in details:
        email = details['Email']
        fname = details['First Name']
        lname = details['Last Name']
        mobile = details['Mobile']
        house = details['House']
        street = details['Street']
        thana = details['Thana']
        district = details['District']
        p_code = details['Postal Code']
        pw = details['Password']
        cpw = details['Confirm']
        ques = details['Question']
        ans = details['Answer']
        hint = details['Hint']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email, ))
        account1 = cur.fetchone()
        cur.execute(f"SELECT * FROM users WHERE phone = %s", (mobile, ))
        account2 = cur.fetchone()
        if account1 or account2:
            msg = 'Account already exists! Try another email or mobile number!'
        elif len(email) == 0 or len(fname) == 0 or len(lname) == 0 or len(mobile) == 0 or len(house) == 0 or len(street) == 0 or len(thana) == 0 or len(district) == 0 or len(p_code) == 0 or len(pw) == 0 or len(cpw) == 0 or len(ques) == 0 or len(ans) == 0 or len(hint) == 0:
            msg = 'Please fill out the form!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif len(mobile) != 11:
            msg = 'Invalid mobile number!'
        elif len(pw) < 8:
            msg = "Password's length must be at least 8!"
        elif len(p_code) != 4:
            msg = 'Invalid post code!'
        elif pw == cpw:
            zero = 0
            cur.execute("INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL, %s, %s, %s, %s, %s, %s, %s, %s)", (email, pw, fname, lname, mobile, ques, ans, hint, zero, zero, zero, street, house, thana, district, p_code, ))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered! You can now log in!'
        else:
            msg = "Please check if the 'Password' and 'Confirm Password' field is different. Those two fields must be equal."
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("signup.html", msg = msg)


if __name__ == '__main__':
    app.run(debug=True)
