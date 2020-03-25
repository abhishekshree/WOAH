from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQ

app = Flask(__name__)
# signed_up = false a variable to restrict free movement


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def loginCheck():
    emailcheck = request.form.get('email')
    password = request.form.get('pass')

    if emailcheck == "woah@gmail.com" and password == "woahwoah":
        return render_template("admin.html")
    else:
        return redirect(url_for('login'))


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/add_music')
def add_music():
    return render_template("addMusic.html")


@app.route('/view_chart')
def view_chart():
    return render_template("viewChart.html")


if __name__ == '__main__':
    app.run(debug=True)
