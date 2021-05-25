import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'database'
app.config['MYSQL_DB'] = 'kemne_jabo'

app.secret_key = 'kemne_jabo'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


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
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        account1 = cur.fetchone()
        cur.execute("SELECT * FROM users WHERE phone = %s", (mobile,))
        account2 = cur.fetchone()
        if account1 or account2:
            msg = 'Account already exists! Try another email or mobile number!'
        elif len(email) == 0 or len(fname) == 0 or len(lname) == 0 or len(mobile) == 0 or len(house) == 0 or len(
                street) == 0 or len(thana) == 0 or len(district) == 0 or len(p_code) == 0 or len(pw) == 0 or len(
            cpw) == 0 or len(ques) == 0 or len(ans) == 0 or len(hint) == 0:
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
            cur.execute(
                "INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    email, pw, fname, lname, mobile, ques, ans, hint, zero, zero, zero, street, house, thana, district,
                    p_code,))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered! You can now log in!'
        else:
            msg = "Please check if the 'Password' and 'Confirm Password' field is different. Those two fields must be equal."
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("signup.html", msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    details = request.form
    msg = ""
    if request.method == 'POST' and 'Email' in details and 'Password' in details:
        email = details['Email']
        pw = details['Password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cur.fetchone()
        if account:
            cur.execute('SELECT * FROM users WHERE email = %s AND pass = %s', (email, pw,))
            account = cur.fetchone()
            if account:
                session['loggedin'] = True
                session['user_id'] = account['user_id']
                session['email'] = account['email']
                return redirect(url_for('profile'))
            else:
                msg = 'Incorrect Password!'
        else:
            msg = 'Incorrect Email ID!'
    return render_template("login.html", msg=msg)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:
        id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM users WHERE user_id = %s', (id,))
        account = cur.fetchone()
        who = account['first_name'] + "'s"
        name = '    ' + account['first_name'] + ' ' + account['last_name']
        email = '    ' + account['email']
        phone = '    ' + account['phone']
        address = '    ' + 'House - ' + account['house'] + ', Street - ' + account['street'] + ', ' + account[
            'thana'] + ', ' + account['district'] + ', ' + account['postal_code'] + '.'
        point = '    ' + str(account['points'])
        balance = '    ' + str(account['money'])
        withdraw = "No"
        if account['can_withdraw'] == 1:
            withdraw = "Yes"
        return render_template('profile.html', who=who, name=name, email=email, phone=phone, address=address,
                               point=point, balance=balance, withdraw=withdraw)
    return render_template('profile.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/faq')
def faq():
    one = 1
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM reports WHERE is_FAQ = %s', (one,))
    info = cur.fetchall()
    return render_template('faq.html', info=info)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    details = request.form
    msg = ""
    if request.method == "POST" and 'name' in details and 'email' in details and 'message' in details:
        name = details['name']
        email = details['email']
        message = details['message']
        if len(name) == 0 or len(email) == 0 or len(message) == 0:
            msg = 'Please fill out the form!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            account = cur.fetchone()
            zero = 0
            one = 1
            cur = mysql.connection.cursor()
            if account:
                cur.execute("INSERT INTO reports VALUES (NULL, %s, NULL, %s, %s, %s)",
                            (message, zero, zero, account['user_id']))
            else:
                cur.execute("INSERT INTO reports VALUES (NULL, %s, NULL, %s, %s, %s)", (message, zero, zero, one))
            msg = 'We have got your message. We will reply soon. Thank you!'
            mysql.connection.commit()
            cur.close()
    return render_template('contact.html', msg=msg)


@app.route('/report', methods=['GET', 'POST'])
def report():
    details = request.form
    msg = ""
    if request.method == "POST" and 'name' in details and 'email' in details and 'message' in details:
        name = details['name']
        email = details['email']
        message = details['message']
        if len(name) == 0 or len(email) == 0 or len(message) == 0:
            msg = 'Please fill out the form!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            account = cur.fetchone()
            zero = 0
            one = 1
            cur = mysql.connection.cursor()
            if account:
                cur.execute("INSERT INTO reports VALUES (NULL, %s, NULL, %s, %s, %s)",
                            (message, zero, zero, account['user_id']))
            else:
                cur.execute("INSERT INTO reports VALUES (NULL, %s, NULL, %s, %s, %s)", (message, zero, zero, one))
            msg = 'We have got your message. We will reply soon. Thank you!'
            mysql.connection.commit()
            cur.close()
    return render_template('report.html', msg=msg)


@app.route('/forgotpw', methods=['GET', 'POST'])
def forgotpw():
    details = request.form
    msg = ""
    if request.method == 'POST' and 'Email' in details:
        email = details['Email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        account = cur.fetchone()
        if account:
            idd = account['user_id']
            return redirect(url_for('recover', idd=idd))
        else:
            msg = 'No such account exists. Please enter a valid Email ID!'
    return render_template("forgotpw.html", msg=msg)


@app.route('/recover/<idd>', methods=['GET', 'POST'])
def recover(idd):
    details = request.form
    msg = ""
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users WHERE user_id = %s", (idd,))
    account = cur.fetchone()
    email = '    ' + account['email']
    ques = '    ' + account['question']
    ans1 = account['answer']
    hint = '    ' + account['hint'] + '.'
    ppw = account['pass']
    if request.method == 'POST' and 'answer' in details and 'Password' in details and 'Confirm' in details:
        ans2 = details['answer']
        pw = details['Password']
        cpw = details['Confirm']
        ans1 = ans1.lstrip()
        ans2 = ans2.lstrip()
        ans1 = ans1.rstrip()
        ans2 = ans2.rstrip()
        ans1 = ans1.lower()
        ans2 = ans2.lower()
        if len(ans2) == 0:
            msg = 'Please enter your answer!'
        elif len(pw) < 8:
            msg = "Password's length must be at least 8!"
        elif ans1 == ans2:
            if pw == cpw:
                if pw == ppw:
                    msg = 'New password cannot be same as previous password. Try again!'
                else:
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE users SET pass = %s WHERE user_id = %s;", (pw, idd,))
                    mysql.connection.commit()
                    cur.close()
                    msg = 'Password changed successfully. You can now login!'
            else:
                msg = "Please check if the 'Password' and 'Confirm Password' field is different. Those two fields must be equal."
        else:
            msg = 'Your answer is wrong. Try again!'
    return render_template("recover.html", idd=idd, email=email, ques=ques, hint=hint, msg=msg)


@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    details = request.form
    msg = ""
    if request.method == 'POST' and 'transport' in details and 'low' in details and 'high' in details and 'start' in details and 'end' in details:
        transport = details['transport']
        low = details['low']
        high = details['high']
        start = details['start']
        end = details['end']
        if len(transport) == 0 or len(low) == 0 or len(high) == 0 or len(start) == 0 or len(end) == 0:
            msg = "Enter all values!"
        else:
            idd = session['user_id']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM information WHERE start_pos = %s AND destination = %s AND user_id = %s", (start, end, idd,))
            account = cur.fetchone()
            if account:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT * FROM mediums m, information i WHERE m.information_id = i.information_id AND transport = %s", (transport,))
                account = cur.fetchone()
                if account:
                    msg = "You have already added this transport for this information!"
                else:
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO mediums VALUES (NULL, %s, %s, %s, %s)", (transport, low, high, account['information_id']))
                    mysql.connection.commit()
                    cur.close()
                    msg = "Your valuable information is added to our database!"
            else:
                zero = 0
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO information VALUES (NULL, %s, %s, %s, %s, %s, %s)", (start, end, zero, zero, zero, session['user_id']))
                mysql.connection.commit()
                cur.close()
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT * FROM information WHERE user_id = %s ORDER BY information_id DESC", (idd,))
                mx = cur.fetchone()
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO mediums VALUES (NULL, %s, %s, %s, %s)", (transport, low, high, mx['information_id']))
                mysql.connection.commit()
                cur.close()
                msg = "Your valuable information is added to our database!"
    return render_template('contribute.html', msg=msg)


@app.route('/search', methods=['GET', 'POST'])
def search():
    details = request.form
    msg = ""
    if request.method == 'POST' and 'start' in details and 'end' in details:
        start = details['start']
        end = details['end']
        if len(start) == 0 or len(end) == 0:
            msg = "Enter both values!"
            return render_template('search.html', msg=msg)
        return redirect(url_for('info', start=start, end=end))
    return render_template('search.html', msg=msg)


@app.route('/info/<start>/<end>', methods=['GET', 'POST'])
def info(start, end):
    zero = 0
    one = 1
    idd = session['user_id']
    msg = ""
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM information i, mediums m, users u WHERE i.start_pos = %s AND i.destination = %s AND i.information_id = m.information_id AND u.user_id = i.user_id", (start, end,))
    account = cur.fetchall()
    cur.execute("SELECT * FROM information WHERE start_pos = %s", (start,))
    account1 = cur.fetchall()
    cur.execute("SELECT * FROM information WHERE destination = %s", (end,))
    account2 = cur.fetchall()
    if not account and not account1 and not account2:
        msg = 'No information available!'
    elif not account and account1 and account2:
        cur.execute("SELECT * FROM information i, mediums m, users u WHERE u.user_id = i.user_id AND m.information_id = i.information_id AND i.start_pos = %s AND i.destination IN (SELECT start_pos FROM information WHERE destination = %s)", (start, end,))
        account1 = cur.fetchall()
        cur.execute("SELECT * FROM information i, mediums m, users u WHERE u.user_id = i.user_id AND m.information_id = i.information_id AND i.destination = %s AND i.start_pos IN (SELECT destination FROM information WHERE start_pos = %s)", (end, start))
        account2 = cur.fetchall()
        account = sum((account1, account2), ())
        if not account:
            msg = 'No information available!'
    if request.method == 'POST':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM information WHERE start_pos = %s AND destination = %s AND on_query = %s", (start, end, one,))
        acc = cur.fetchone()
        if acc:
            cur.execute("SELECT * FROM taken_by WHERE information_id = %s AND user_id = %s", (acc['information_id'], idd,))
            ac = cur.fetchone()
            if not ac:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO taken_by VALUES (NULL, %s, %s, %s)", (zero, acc['information_id'], idd,))
                mysql.connection.commit()
                cur.close()
            msg = 'This information is already on query. Please keep an eye on notifications to see if it is answered by any guide!'
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO information VALUES (NULL, %s, %s, %s, %s, %s, %s)", (start, end, zero, zero, one, one))
            mysql.connection.commit()
            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO taken_by VALUES (NULL, %s, %s, %s)", (zero, acc['information_id'], idd,))
            mysql.connection.commit()
            cur.close()
            msg = 'Added to query. Please keep an eye on notifications to see if it is answered by any guide!'
    elif request.method == 'GET':
        for ac in account:
            if ac['user_id'] != idd:
                cur.execute("SELECT * FROM users WHERE user_id = %s", (ac['user_id'],))
                temp = cur.fetchone()
                point = temp['points'] + 10
                money = point * 0.01
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET points = %s, money = %s WHERE user_id = %s;",
                            (point, money, temp['user_id'],))
                mysql.connection.commit()
                cur.close()
                if point >= 10000:
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE users SET can_withdraw = %s WHERE user_id = %s;", (one, temp['user_id'],))
                    mysql.connection.commit()
                    cur.close()
    return render_template('info.html', msg=msg, start=start, end=end, account=account)


if __name__ == '__main__':
    app.run(debug=True)
