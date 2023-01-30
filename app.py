from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask import Blueprint, render_template, request, redirect, url_for
import json

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app1 = Flask(__name__)
    app1.register_blueprint(views, url_prefix="/")
    app1.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app1)

    with app1.app_context():
        db.create_all()
    return app1

from flask_login import UserMixin
views = Blueprint(__name__, "views")


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout =db.Column(db.String(10))
    weight = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    username = db.Column(db.String(15), db.ForeignKey('user.username'))

class User(db.Model):
    username = db.Column(db.String(15), primary_key=True)
    


@views.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        workout = str(request.form['workout'])
        weight = str(request.form['weight'])
        reps = str(request.form['reps'])
        username = str(request.form['username'])
        newWorkout = Workout(workout=workout, weight=weight, reps=reps, username=username)
        db.session.add(newWorkout)
        db.session.commit()

        message = "You did " + workout + " at " + weight + " pounds for " + reps + " reps"
        return redirect(url_for('__main__.workouts'))
        # render_template("index.html", message=message)
    else:
        return render_template("index.html", message = 'None')


@views.route("/create/<username>", methods=['GET', 'POST'])
def create(username):
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    
    return username + " Account Created"

#Shows all the users in the User table
@views.route("/users", methods= ['GET', 'POST'])
def users():
    users = User.query.all()
    usersString = ""
    for user in users:
        usersString += (user.username + "<br/>")
    print(users)
    return render_template("users.html", users= users)

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
@views.route("/workouts", defaults = {'username':None})
@views.route("/workouts/<username>")
def workouts(username):
    
    if username:
        foundWorkouts = Workout.query.filter(Workout.username == username)
    else:
        foundWorkouts = Workout.query.all()
    users = User.query.all()
    return render_template("workouts.html", workouts = foundWorkouts, users=users)

@views.route("/info")
def info():
    return "Welcome to the info page."

if __name__=='__main__':
    app1 = create_app()
    app1.run(debug=True)

