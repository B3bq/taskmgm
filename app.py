from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()  # ładowanie zmiennych z pliku .env

app = Flask(__name__)

# konfiguracja bazy
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
db = SQLAlchemy(app)

# model ORM
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

# create table in base
with app.app_context():
    db.create_all()

# main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/success/<name>')
def success(name):
    return f'siema {name}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        password = request.form['password']
        print('wzial')

        # taking values from database
        with app.app_context():
            db_name = Users.query.with_entities(Users.name).filter_by(name=user).scalar()
            db_pass = Users.query.with_entities(Users.password).filter_by(name=user).scalar()

        if user == db_name and bcrypt.checkpw(password.encode('utf-8'), db_pass.encode('utf-8')):
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))
    else:
        print('te czesc')
        user = request.args.get('nm')
        return "redirect(url_for('success', name=user))"

@app.route('/form')
def sign():
    return render_template('sign.html')

@app.route('/sign', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        user = request.form['name']
        mail = request.form['email']
        password = request.form['password']
        rpassword = request.form['re_password']

        if password == rpassword:
            print('zgadza sie')
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_str = hashed.decode('utf-8')
            with app.app_context():
                new_user = Users(name=user, email=mail, password=hashed_str)
                db.session.add(new_user)
                db.session.commit()
                print('dodano')
                return "<p>Added user</p><a href='/'><button>Back</button></a>"
        else:
            print('nie zgadza sie')
            return render_template('sign.html')
    else:
        return "nic"

if __name__ == "__main__":
    app.run(debug=True)
