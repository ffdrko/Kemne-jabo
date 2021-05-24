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


@app.route('/', methods=['GET', 'POST'])
def index():
    details = request.form
    msg = ""
    if request.method == 'POST':
        pw = details['Password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM admins WHERE pass = %s", (pw,))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            return redirect(url_for('admin_profile'))
        else:
            msg = 'Incorrect Password!'
    return render_template('admin_login.html', msg=msg)


@app.route('/admin_logout')
def admin_logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/admin_profile')
def admin_profile():
    zero = 0
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM reports WHERE is_ans = %s", (zero,))
    account = cur.fetchall()
    msg = ""
    if account:
        return render_template('admin_profile.html', account=account, msg=msg)
    else:
        msg = 'No more reports!'
        return render_template('admin_profile.html', account=account, msg=msg)


@app.route('/feedback/<report_id>', methods=['GET', 'POST'])
def feedback(report_id):
    if request.method == 'POST':
        details = request.form
        msg = details['message']
        val = details['faq']
        one = 1
        cur = mysql.connection.cursor()
        if val == 'checked':
            cur.execute("UPDATE reports SET is_ans = %s, feedback = %s, is_FAQ = %s WHERE report_id = %s", (one, msg, one, report_id,))
        else:
            cur.execute("UPDATE reports SET is_ans = %s, feedback = %s WHERE report_id = %s",(one, msg, report_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('admin_profile'))
    else:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM reports WHERE report_id = %s", (report_id,))
        account = cur.fetchone()
        return render_template("feedback.html", account=account)


if __name__ == '__main__':
    app.run(debug=True)
