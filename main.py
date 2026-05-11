from flask import Flask, redirect, render_template, request

app = Flask(__name__)

#@app.route("/register")
#@app.route("/login")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/basics")
def basics():
    return render_template("basics.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/development")
def development():
    return render_template("development.html")

@app.route("/stories")
def stories():
    return render_template("stories")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot")




app.run(host="127.0.0.1", debug=True)