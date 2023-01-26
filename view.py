from flask import Blueprint, render_template,request


views = Blueprint(__name__, "views")


from app import User, db


workouts = []
@views.route("/", methods=['GET', 'POST'])
def home():
    
    if request.method == "POST":
        workout = str(request.form['workout'])
        weight = str(request.form['weight'])
        reps = str(request.form['reps'])
        message = "You did " + workout + " at " + weight + " pounds for " + reps + " reps"
        workouts.append(message)
        print(workouts)
        return render_template("index.html", message=message, workouts=workouts)
    else:
        return render_template("index.html", message = 'None')


@views.route("/create", methods=['GET', 'POST'])
def create():
    new_user = User(username="Brandon")
    db.session.add(new_user)
    
    db.session.commit()
    
    return "Account Created"


@views.route("/info")
def info():
    return "Welcome to the info page. This application was built to practice web development."