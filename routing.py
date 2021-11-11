#ITSC3155 Project

#Imports
import os
from flask import Flask, render_template, request, redirect, url_for
from databse import db
from models import Question
from models import User

#Create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aardvark_answers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Bind SQLAlchemy db object to this Flask app
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
    questions = db.session.query(Question).All()

    return render_template('questions.html', Question = questions)

@app.route('/newQuestion', method=['GET', 'POST'])
def newQuestion():
    #this needs to be able to post a new question
    if request.method == 'POST':
        header = request.form['header']
        body = request.form['body']
        #user = ....
        #likes = ....
        #dislikes = .....
        #topics are a list? does this need to be an array
        topics = request.form['topics']
        #imageURL = ....

        #Add new question to database
        new_question = Question(header, body, user, likes, dislikes, topics, imageURL)
        db.session.add(new_record)
        db.session.commit()
    else:
        return render_template('newQuestion.html')

        return redirect(url_for('newQuestion'))

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
