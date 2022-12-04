from flask import Blueprint, render_template

views = Blueprint(__name__, "views")


#Can pass variables like username with the render template function
@views.route("/")
def home():
    return render_template("index.html", username = "Brandon")

@views.route("/info")
def info():
    return "Welcome to the info page. This application was built to practice."