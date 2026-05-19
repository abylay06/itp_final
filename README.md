🌸 MomGuide — A Web Guide for New Mothers
MomGuide is a Flask-based web application designed to support new mothers through their first year of motherhood. It provides essential baby care information, an interactive quiz, a baby milestone tracker, a community stories board, and an AI-powered chatbot — all in one place.

🚀 Live Demo
👉 https://itp-final.onrender.com/

✨ Features


Baby Basics — 10 essential rules every new mother should know

Knowledge Quiz — 10-question quiz with instant scoring and result saved to CSV

Milestone Tracker — Month-by-month baby development guide (Month 1 to 12)

Mom Stories — Community board where mothers can share and read experiences (stored in JSON)

AI Chatbot — Ask any baby care question powered by Groq's LLaMA 3 model


🛠️ Technologies Used
CategoryTechnologyBackendPython 3, FlaskFrontendHTML5, CSS3, Jinja2 TemplatesAI ChatbotGroq API (LLaMA 3.3 70B)Data StorageJSON (stories), CSV (quiz results)OOP ConceptsClasses, Inheritance, Decorators, GeneratorTestingPython unittestDeploymentRender

📁 Project Structure
momguide/
├── main.py               # Flask app — routes, classes, logic
├── test_app.py           # Unit tests
├── stories.json          # Stored community stories
├── quiz_results.csv      # Stored quiz scores
├── static/
│   └── style.css         # All styling
└── templates/
    ├── layout.html        # Base template
    ├── index.html         # Home page
    ├── basics.html        # Baby basics page
    ├── quiz.html          # Quiz page
    ├── quiz_result.html   # Quiz result page
    ├── development.html   # Milestones page
    ├── stories.html       # Stories page
    └── chatbot.html       # AI chatbot page

▶️ How to Run

The project is deployed and accessible at:

👉 https://itp-final.onrender.com/

Simply open the link in any browser — no installation needed.
