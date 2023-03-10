from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app1 = Flask(__name__)
    app1.register_blueprint(views, url_prefix="/")
    app1.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app1.config['SECRET_KEY'] = 'super secret key'
    db.init_app(app1)

    login_manager = LoginManager()
    login_manager.login_view = '/login'
    login_manager.init_app(app1)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    with app1.app_context():
        db.create_all()
    return app1

from flask_login import UserMixin
views = Blueprint(__name__, "views")

def getCurrentUser():
    if current_user.is_active:
        cUser = current_user.username
    else:
        cUser = None
    return cUser

#The model for the workout
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout =db.Column(db.String(10))
    weight = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    username = db.Column(db.String(15), db.ForeignKey('user.username'))

#The model for user profiles
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    password = db.Column(db.String(15))
    

#The home page
@views.route("/", methods=['GET', 'POST'])
def home():
    cUser = getCurrentUser()
    if request.method == "POST":
        if cUser == None:
            return redirect(url_for('__main__.home'))
        workout = str(request.form['workout'])
        weight = str(request.form['weight'])
        reps = str(request.form['reps'])
        newWorkout = Workout(workout=workout, weight=weight, reps=reps, username=cUser)
        db.session.add(newWorkout)
        db.session.commit()

        return redirect("/")
    else:
        return render_template("index.html", message = 'None', cUser = cUser)


@views.route("/create/<username>", methods=['GET', 'POST'])
def create(username):
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    
    return username + " Account Created"

@views.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])

        user = User.query.filter_by(username=username).first() 
        if user != None:
            if user.password == password:
                login_user(user)
                return redirect("/")
    cUser = getCurrentUser()
    return render_template("login.html", cUser=cUser)

@views.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

@views.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        userExist = db.session.query(User.username).filter_by(username=username).first() is not None

        if not userExist:
            newUser = User(username=username, password = password)
            db.session.add(newUser)
            db.session.commit()
        else:
            flash('This user already exists!')
            return redirect("/register")
        return redirect("/")
    cUser = getCurrentUser()
    return render_template("signup.html", cUser = cUser)

#Shows all the users in the User table
@views.route("/users", methods= ['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    usersString = ""
    for user in users:
        usersString += (user.username + "<br/>")
    print(users)
    cUser = getCurrentUser()
    return render_template("users.html", users= users, cUser = cUser)

#Deletes all the users in the User table
@views.route("/delete")
def delete():
    usersDeleted = User.query.delete()
    db.session.commit()

    return str(usersDeleted) + " were deleted from the database."

@views.route("/delete/<id>", methods=["GET"])
def deleteId(id):
    workout = Workout.query.get(id)
    db.session.delete(workout)
    db.session.commit()

    return redirect('/workouts')

#Shows all the workouts in the Workout table
#Gather the users and all the stored workouts to send to the workouts page
@views.route("/workouts")
@login_required
def workouts():
    cUser = getCurrentUser()
    if cUser != None:
        foundWorkouts = Workout.query.filter_by(username=cUser).all()
    else:
        foundWorkouts = Workout.query.all()
    users = User.query.all()
    

    return render_template("workouts.html", workouts = foundWorkouts, users=users, cUser=cUser)

@views.route("/info")
def info():
    return "Welcome to the info page."

app1 = create_app()

if __name__=='__main__':
    app1.run(debug=True)

