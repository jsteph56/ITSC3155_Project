# ITSC3155 Project

# Imports
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
    db.create_all()  # run under the app context


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/questions')
def questions():
    # Retrieve user from the database
    a_user = db.session.query(User).filter_by(email='Aardvark@uncc.edu').one()
    # Retrieve list of questions from database
    my_questions = db.session.query(Question).all()

    return render_template('questions.html', question=my_questions, user=a_user)


@app.route('/new_question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        # Get question data
        header = request.form['header']
        body = request.form['body']
        # topics are a list? does this need to be an array
        topics = request.form['topics']
        # imageURL = request.form['imageURL'] - implement at a later date

        from datetime import date
        today = date.today()
        today = today.strftime("%m-%d-%Y")

        # Create a new question
        new_record = Question(header, body, today, topics)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('questions'))
    else:
        # GET request - show new question form
        # Retrieve user from db
        a_user = db.session.query(User).filter_by(email='Aardvark@uncc.edu').one()
        return render_template('new_question.html', user=a_user)


@app.route('/questions/edit/<question_id>', methods=['GET', 'POST'])
def update_question(question_id):
    # Check method used for request
    if request.method == 'POST':
        # Get question data
        header = request.form['header']
        body = request.form['body']
        topics = request.form['topics']

        question = db.session.query(Question).filter_by(id=question_id).one()

        # Update question data
        question.header = header
        question.body = body
        question.topics = topics
        # Update note in db
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('questions'))
    else:
        # GET request - show new question form to edit question details
        # Retrieve user from database
        a_user = db.session.query(User).filter_by(email='Aardvark@uncc.edu').one()
        # Retrieve question from database
        my_question = db.session.query(Question).filter_by(id=question_id).one()

        return render_template('new_question.html', question=my_question, user=a_user)


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
