#ITSC3155 Project

#Imports
import os
from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import Question as Question
from models import User as User

# Create the app
app = Flask(__name__)

# Set name and location of database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aardvark_answers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/questions')
def questions():
    #this is the same as get_notes, we just need to retrieve the notes from the database to display them

    #retrieve list of questions from database
    questions = db.session.query(Question).all()

    return render_template('questions.html', Question=questions)

@app.route('/new_question', methods=['GET', 'POST'])
def new_question():
    # this needs to be able to post a new question
    if request.method == 'POST':
        # Get question data
        header = request.form['header']
        body = request.form['body']
        user = request.form['user']
        likes = request.form['likes']
        dislikes = request.form['dislikes']
        #topics are a list? does this need to be an array
        topics = request.form['topics']
        imageURL = request.form['imageURL']

        # Create a new question
        new_question = Question(header, body, user, likes, dislikes, topics, imageURL)
        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for('questions'))
    else:
        # GET request - show new question form
        return render_template('new_question.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
