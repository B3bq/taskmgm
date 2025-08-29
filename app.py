from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
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
    coins = db.Column(db.Integer, nullable=False, server_default="0")
    pet = db.relationship("Pet", backref="owner")
    tasks = db.relationship("Tasks", backref="owner")

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, server_default='new')
    category = db.Column(db.String(50), nullable=False)
    repeatability = db.Column(db.Date, nullable=False)

class Gifs(db.Model):
    __tablename__ = 'gifs'
    id = db.Column(db.Integer, primary_key=True)
    min = db.Column(db.Integer, nullable=False)
    max = db.Column(db.Integer, nullable=False)
    gif_url = db.Column(db.String(255), nullable=False)
    pet = db.Column(db.String(50), nullable=False)
    pets = db.relationship("Pet", backref="gif")

class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    gif_id = db.Column(db.Integer, db.ForeignKey('gifs.id'), server_default='4')
    pet = db.Column(db.String(50), server_default='panda')
    name = db.Column(db.String(50), nullable=False, server_default='Ryszard')
    feed = db.Column(db.Integer, nullable=False, server_default="100")

# create table in base
with app.app_context():
    db.create_all()

# main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main/<user>')
def main(user):
    print(user)

    with app.app_context():
        #take user data
        user_data = Users.query.filter(Users.name == user).first()

        tasks = user_data.tasks

        user_pet = user_data.pet[0] if user_data.pet else None

        if not user_pet:
            user_pet = Pet(user_id=user_data.id)
            db.session.add(user_pet)
            db.session.commit()

        user_data = Users.query.filter(Users.name == user).first()

        tasks = user_data.tasks

        user_pet = user_data.pet[0] if user_data.pet else None

        gif = Gifs.query.filter(
            and_(
                Gifs.min < user_pet.feed,
                Gifs.max >= user_pet.feed,
                Gifs.pet == user_pet.pet
            )
        ).first()

        if user_pet.feed == 0 :
            src = 'img/pet/basket.png'
        elif user_pet.feed <= 20:
            src = 'img/pet/1bamboo.png'
        elif user_pet.feed <= 40:
            src = 'img/pet/2bamboo.png'
        elif user_pet.feed <= 60:
            src = 'img/pet/3bamboo.png'
        elif user_pet.feed <= 80:
            src = 'img/pet/4bamboo.png'
        else:
            src = 'img/pet/5bamboo.png'

        

    return render_template('main.html', tasks=tasks, user_pet=user_pet, gif=gif, user=user_data, src=src)

@app.route('/tasks/<user>')
def tasks(user):
    user_data = Users.query.filter(Users.name == user).first()

    tasks = user_data.tasks 

    return render_template('tasks.html', user=user_data, tasks=tasks)

@app.route('/task/<user>')
def task(user):
    user_data = Users.query.filter(Users.name == user).first()

    return render_template('task.html', user=user_data)

@app.route('/success/<name>')
def success(name):
    return f'siema {name}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        password = request.form['password']

        # taking values from database
        with app.app_context():
            db_name = Users.query.with_entities(Users.name).filter_by(name=user).scalar()
            db_pass = Users.query.with_entities(Users.password).filter_by(name=user).scalar()

        if user == db_name and bcrypt.checkpw(password.encode('utf-8'), db_pass.encode('utf-8')):
            return redirect(url_for('main', user=user))
        else:
            return redirect(url_for('login'))
    else:
        print('te czesc')
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

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
