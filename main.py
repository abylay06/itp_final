import json, csv, os
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect
from groq import Groq

app = Flask(__name__)

# Decorator
def log_route(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {request.path}")
        return func(*args, **kwargs)
    return wrapper

# Base Class
class DataHandler:
    def __init__(self, filepath):
        self.filepath = filepath
    def load(self):
        raise NotImplementedError
    def save(self, data):
        raise NotImplementedError

# JSON Handler
class JSONDataHandler(DataHandler):
    def load(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    def save(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

# CSV Handler
class CSVDataHandler(DataHandler):
    def __init__(self, filepath, fieldnames):
        super().__init__(filepath)
        self.fieldnames = fieldnames
    def load(self):
        try:
            with open(self.filepath, "r") as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            return []
    def save(self, row):
        exists = os.path.exists(self.filepath)
        with open(self.filepath, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            if not exists:
                writer.writeheader()
            writer.writerow(row)

# Story Manager
class StoryManager(JSONDataHandler):
    def __init__(self):
        super().__init__("stories.json")
    def add(self, author, content):
        stories = self.load()
        stories.insert(0, {
            "author": author,
            "content": content,
            "date": datetime.now().strftime("%b %d, %Y")
        })
        self.save(stories)

# Quiz Manager
class QuizManager(CSVDataHandler):
    ANSWERS = {"q1":"2","q2":"1","q3":"0","q4":"2","q5":"1",
               "q6":"0","q7":"1","q8":"0","q9":"0","q10":"0"}
    def __init__(self):
        super().__init__("quiz_results.csv", ["name","score","date"])
    def grade(self, form):
        return sum(1 for q,a in self.ANSWERS.items() if form.get(q)==a)
    def record(self, name, score):
        self.save({"name":name,"score":score,"date":datetime.now().strftime("%Y-%m-%d")})

# Chatbot 
class Chatbot:
    SYSTEM = "You are a helpful assistant for new mothers. Answer questions about baby care, sleep, feeding, and wellbeing in 3-4 sentences. Recommend a doctor for medical concerns."
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    def ask(self, question):
        res = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content":self.SYSTEM},
                      {"role":"user","content":question}],
            max_tokens=400
        )
        return res.choices[0].message.content

# Milestones generator
def milestones_generator():
    data = [
        {"emoji":"🌱", "title":"Month 1",  "points":["Recognises parents' voices","Sleeps most of the day","Makes small sounds"]},
        {"emoji":"😊", "title":"Month 3",  "points":["Smiles at people","Follows objects with eyes","Holds head up"]},
        {"emoji":"🎉", "title":"Month 6",  "points":["Rolls over","Sits with support","Responds to name"]},
        {"emoji":"🚀", "title":"Month 9",  "points":["Crawls around","Understands simple words","Stands with support"]},
        {"emoji":"🎂", "title":"Month 12", "points":["May take first steps","Says first words","Waves goodbye"]},
    ]
    for item in data:
        yield item

# Init
stories = StoryManager()
quiz    = QuizManager()
bot     = Chatbot()

# Routes 
@app.route("/")
@log_route
def index():
    return render_template("index.html")

@app.route("/basics")
@log_route
def basics():
    return render_template("basics.html")

@app.route("/quiz", methods=["GET","POST"])
@log_route
def quiz_page():
    if request.method == "POST":
        name  = request.form.get("name","Anonymous").strip() or "Anonymous"
        score = quiz.grade(request.form)
        quiz.record(name, score)
        return render_template("quiz_result.html", name=name, score=score)
    return render_template("quiz.html")

@app.route("/development")
@log_route
def development():
    return render_template("development.html", milestones=list(milestones_generator()))

@app.route("/stories", methods=["GET","POST"])
@log_route
def stories_page():
    if request.method == "POST":
        author  = request.form.get("author","Anonymous").strip() or "Anonymous"
        content = request.form.get("story","").strip()
        if content:
            stories.add(author, content)
        return redirect("/stories")
    return render_template("stories.html", stories=stories.load())

@app.route("/chatbot", methods=["GET","POST"])
@log_route
def chatbot_page():
    question, answer = None, None
    if request.method == "POST":
        question = request.form.get("question","").strip()
        if question:
            try:
                answer = bot.ask(question)
            except Exception as e:
                answer = f"Error: {e}"
    return render_template("chatbot.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)