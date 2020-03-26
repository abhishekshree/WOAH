from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# signed_up = false a variable to restrict free movement
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
db.init_app(app)


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
    


@app.route('/')
def main():
    Flist = Final.query.all()
    return render_template("index.html", flist=Flist)


@app.route('/', methods= ['POST'])
def getData():
    sname = request.form.get('songname')
    singer = request.form.get('singer')
    user = request.form.get('uname')
    new_rec = Recommendations(Song_name=sname, Singer_name=singer, rec_name=user)
    db.session.add(new_rec)
    db.session.commit()

    return redirect(url_for('main'))

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def loginCheck():
    emailcheck = request.form.get('email')
    password = request.form.get('pass')

    if emailcheck == "woah@gmail.com" and password == "woahwoah":
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))


@app.route('/admin')
def admin():
    recommendations = Recommendations.query.all()
    return render_template("admin.html", recommendations=recommendations)

@app.route('/drop_song/<string:id>')
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
def add_music():
    return render_template("addMusic.html")

@app.route('/add_music', methods=['POST'])
def add_music_admin():
    sname = request.form.get('sname')
    singer = request.form.get('singer')
    new_rec = Final(Song=sname, singer=singer,givenby="ADMIN" )
    db.session.add(new_rec)
    db.session.commit()

    return redirect(url_for('add_music'))

@app.route('/view_chart')
def view_chart():
    final = Final.query.all()
    return render_template("viewChart.html", final=final)


@app.route('/delete/<string:id>')
def delete(id):
    waste = Final.query.filter_by(id=id).first()
    db.session.delete(waste)
    db.session.commit()

    return redirect(url_for('view_chart'))


if __name__ == '__main__':
    app.run(debug=True)
