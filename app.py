from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
import os, bcrypt, random
from datetime import datetime, timedelta
from dotenv import load_dotenv

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
    reward = db.Column(db.Integer, nullable=False)
    repeatability = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

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
    feed_time = db.Column(db.DateTime, nullable=False, server_default=func.now())

# create table in base
with app.app_context():
    db.create_all()


with app.app_context():
    pets = Pet.query.all()
    tasks = Tasks.query.all()

    today = datetime.today().date()

    for task in tasks:
        if task.repeatability == "daily":
            task.start_date = today
            task.end_date = today + timedelta(days=1)
            task.status = "new"
        elif task.repeatability == "weekly":
            while task.end_date < today:
                task.start_date += timedelta(days=7)
                task.end_date += timedelta(days=7)
                task.status = "new"

    for pet in pets:
        if pet.feed > 0:
            hours_passed = (datetime.now() - pet.feed_time).total_seconds() // 3600
            feed_loss = int(hours_passed*5)
            pet.feed = max(0, pet.feed - feed_loss)
        else:
            pet.feed = 0

    db.session.commit()

# main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main/<user>')
def main(user):
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

@app.route('/increase/<user>/<int:user_coins>/<int:pet_id>', methods=['POST'])
def increase_feed(user, user_coins, pet_id):
    pet = Pet.query.get_or_404(pet_id)
    user_data = Users.query.filter(Users.name == user).first()
    if user_coins > 0 and pet.feed < 100:    
        pet.feed += 20
        user_data.coins -= 20
        pet.feed_time = datetime.now()
        db.session.commit()
    return redirect(url_for("main", user=user))

@app.route('/update_name/<user>/<int:pet_id>', methods=['POST'])
def update_name(user, pet_id):
    new_name = request.form['new_name']
    pet = Pet.query.get_or_404(pet_id)
    pet.name = new_name
    db.session.commit()
    return redirect(url_for('main', user=user))

@app.route('/all_tasks/<user>')
def all_tasks(user):
    user_data = Users.query.filter(Users.name == user).first()
    tasks = user_data.tasks

    return render_template('user_tasks.html', tasks=tasks, user=user_data)

@app.route('/tasks/<user>')
def tasks(user):
    today = datetime.today().date()
    user_data = Users.query.filter(Users.name == user).first()

    tasks = Tasks.query.filter(Tasks.user_id == user_data.id, Tasks.start_date <= today, Tasks.end_date >= today).all()

    return render_template('tasks.html', user=user_data, tasks=tasks)

@app.route('/update_status', methods=["POST"])
def update_status():
    data = request.get_json()
    task_id = data.get("id")
    new_status = data.get("status")
    user_id = data.get("userID")

    task = Tasks.query.get(task_id)

    if task:
        old_status = task.status
        task.status = new_status
        if task.status == "done" and old_status != "done":
            user = Users.query.get(user_id)
            user.coins += task.reward
        db.session.commit()
        return jsonify({"success": True, "id": task.id, "status": task.status})
    return jsonify({"success": False, "error": "Task not found"}), 404

@app.route('/delete_task', methods=["POST"])
def delete_task():
    data = request.get_json()
    task_id = data.get("id")
    user = data.get("userName")
    link = data.get("from")

    task = Tasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    if link == "tasks":
        return jsonify({"success": True, "redirect": url_for("tasks", user=user)})
    else:
        return jsonify({"success": True, "redirect": url_for("all_tasks", user=user)})

@app.route('/delete/<user>', methods=["POST"])
def delete(user):
    task_id = request.form['delete']

    user_data = Users.query.filter(Users.name == user).first()
    task = Tasks.query.get_or_404(task_id)

    if user_data.coins >= 40:
        user_data.coins -= 40
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for('main', user=user))

@app.route('/task/<user>')
def task(user):
    user_data = Users.query.filter(Users.name == user).first()

    return render_template('task.html', user=user_data)

@app.route('/add_task/<int:user_id>/<user>', methods=['POST'])
def add_task(user_id, user):
    # data from html
    name = request.form['name']
    des = request.form['description']
    prio = request.form['priority']
    repeatability = request.form['option']
    
    match repeatability:
        case "daily":
            start_date = datetime.today().date()
            end_str = "2073-04-28"
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
        case "weekly":
            start_date_str = request.form['weekly']
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = start_date + timedelta(days=1)
        case _:
            date_str = request.form['range'].strip()
    
            if ' - ' in date_str:
                start_str, end_str = date_str.split(' - ')
            elif '-' in date_str:  # fallback na samą jedną datę
                start_str = end_str = date_str
            else:
                raise ValueError(f"Unexpected date format: {date_str}")
            start_date = datetime.strptime(start_str.strip(), "%Y-%m-%d").date()
            end_date = datetime.strptime(end_str.strip(), "%Y-%m-%d").date()
        
    match prio:
        case 'critical':
            reward = random.randint(35, 50)
        case 'important':
            reward = random.randint(20, 40)
        case 'medium':
            reward = random.randint(10, 25)
        case 'low':
            reward = random.randint(5, 15)
        case _:
            reward = random.randint(1, 10)

    with app.app_context():
        new_task = Tasks(user_id=user_id, name=name, description=des, category=prio, reward=reward, repeatability=repeatability, start_date=start_date, end_date=end_date)    
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('tasks', user=user))

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
                
                return "<p>Added user</p><a href='/'><button>Back</button></a>"
        else:
            print('nie zgadza sie')
            return render_template('sign.html')
    else:
        return "nic"

if __name__ == "__main__":
    app.run(debug=True)
