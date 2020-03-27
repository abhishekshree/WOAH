from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
import flask_login


app = Flask(__name__)
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SECRET_KEY'] = "nahibataengetumkokuchbhibeta"
db.init_app(app)

#Models

class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Song_name = db.Column(db.String(100))
    Singer_name = db.Column(db.String(100))
    rec_name = db.Column(db.String(100))


class Final(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Song = db.Column(db.String(100))
    singer = db.Column(db.String(100))
    givenby = db.Column(db.String(100))
    

users = {
    "woah@gmail.com":"woahwoah",
    "user@gmail.com":"bye"
}

#UserMixin
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

# Main Views
global get
get=False

global loginMessage
loginMessage=False


@app.route('/')
def main():
    Flist = Final.query.all()
    return render_template("index.html", flist=Flist, get=get)


@app.route('/', methods= ['POST'])
def getData():
    
    sname = request.form.get('songname')
    singer = request.form.get('singer')
    user = request.form.get('uname')
    new_rec = Recommendations(Song_name=sname, Singer_name=singer, rec_name=user)
    db.session.add(new_rec)
    db.session.commit()
    global get
    get=True

    return redirect(url_for('main'))


@app.route('/login')
def login():
    return render_template("login.html", loginMessage=loginMessage)


@app.route('/logout')
def logout():
     flask_login.logout_user()
     return redirect(url_for('main'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/login', methods=['POST'])
def loginCheck():
    emailcheck = request.form.get('email')
    password = request.form.get('pass')

    if emailcheck in users and users.get(emailcheck) == password:
        
        user = User()
        user.id = emailcheck
        flask_login.login_user(user)
        return redirect(url_for('admin'))
    else:
        global loginMessage
        loginMessage = True
        return redirect(url_for('login'))


@app.route('/admin')
@flask_login.login_required
def admin():
    recommendations = Recommendations.query.all()
    return render_template("admin.html", recommendations=recommendations)


@app.route('/drop_song/<string:id>')
@flask_login.login_required
def drop_song(id):
    waste = Recommendations.query.filter_by(id=id).first()
    db.session.delete(waste)
    db.session.commit()

    return redirect(url_for('admin'))


@app.route('/to_chart/<string:id>')
def to_chart(id):
    song = Recommendations.query.filter_by(id=id).first()
    finalUp = Final(Song=song.Song_name, singer=song.Singer_name, givenby=song.rec_name)
    db.session.add(finalUp)
    db.session.commit()
    drop_song(id)
    return redirect(url_for('view_chart'))


@app.route('/add_music')
@flask_login.login_required
def add_music():
    return render_template("addMusic.html")

@app.route('/add_music', methods=['POST'])
@flask_login.login_required
def add_music_admin():
    sname = request.form.get('sname')
    singer = request.form.get('singer')
    new_rec = Final(Song=sname, singer=singer,givenby="ADMIN" )
    db.session.add(new_rec)
    db.session.commit()

    return redirect(url_for('add_music'))

@app.route('/view_chart')
@flask_login.login_required
def view_chart():
    final = Final.query.all()
    return render_template("viewChart.html", final=final)


@app.route('/delete/<string:id>')
@flask_login.login_required
def delete(id):
    waste = Final.query.filter_by(id=id).first()
    db.session.delete(waste)
    db.session.commit()

    return redirect(url_for('view_chart'))


if __name__ == '__main__':
    app.run(debug=True)
