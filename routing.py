# ITSC3155 Project

# Imports
import os
from flask import Flask, flash, render_template, request, redirect, url_for, session
from database import db
from models import Question as Question, Review
from models import User as User
from models import Comment as Comment
from models import Like as Like
from models import Dislike as Dislike
from forms import RegisterForm, LoginForm, CommentForm, SearchForm
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import bcrypt

UPLOAD_FOLDER = 'static\Images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# Create the app
app = Flask(__name__)

# Set name and location of database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aardvark_answers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Secret key
app.config['SECRET_KEY'] = 'SE3155'

# Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()  # run under the app context


@app.route('/')
@app.route('/index')
def index():
    # Check if a user is saved in session
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    return render_template('index.html')


@app.route('/questions')
def questions():
    # Check if user is saved in session
    search = SearchForm()

    if request.method == 'POST' and search.validate_on_submit():
        return redirect((url_for('search_results', result=search.search.data)))

    if session.get('user'):
        # Retrieve questions from database
        all_users = db.session.query(User).all()

        all_questions = db.session.query(Question).all()
        user_questions = db.session.query(Question).filter_by(user_id=session['user_id']).all()

        return render_template('questions.html', questions=all_questions, user_questions=user_questions,
                               user=session['user'], users=all_users)
    else:
        # Redirect user to login view
        return redirect(url_for('login'))

@app.route('/questions/search_results')
def search_results(result):
    results = User.query.whoosh_search(result).all()
    form = SearchForm()
    return render_template('view_question.html', question=results, user=session['user'], form=form)


@app.route('/questions/<question_id>')
def view_question(question_id):
    # Check if user is saved in session
    if session.get('user'):
        # Retrieve note from database
        my_questions = db.session.query(Question).filter_by(id=question_id).one()
        my_user = db.session.query(User).filter_by(id=session['user_id']).first()
        # Create a comment form object
        form = CommentForm()

        return render_template('view_question.html', question=my_questions, user=session['user'], my_user=my_user, form=form)
    else:
        return redirect(url_for('login'))


@app.route('/new_question', methods=['GET', 'POST'])
def new_question():
    # Check if user is saved in session
    if session.get('user'):
        # Check method used for request
        if request.method == 'POST':
            # Get question detail data
            header = request.form['header']
            body = request.form['body']
            topics = request.form['topics']
            # Get data stamp
            from datetime import date
            today = date.today()
            # Format date mm/dd/yyy
            today = today.strftime("%m-%d-%Y")
            # Get the last ID used and increment by 1
            # Create new question
            new_record = Question(header, body, today, topics, session['user_id'])
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('questions'))
        else:
            # GET request - show new question form
            return render_template('new_question.html', user=session['user'])
    else:
        # User is not in session, so redirect to login
        return redirect(url_for('login'))


@app.route('/questions/edit/<question_id>', methods=['GET', 'POST'])
def update_question(question_id):
    # Check if user is saved in session
    if session.get('user'):
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
            my_question = db.session.query(Question).filter_by(id=question_id).one()

            return render_template('new_question.html', question=my_question, user=session['user'])


@app.route('/delete/<question_id>', methods=['POST'])
def delete_question(question_id):
    # Check if a user is saved in session
    if session.get('user'):
        # Retrieve question from database
        my_question = db.session.query(Question).filter_by(id=question_id).one()

        db.session.delete(my_question)
        db.session.commit()

        return redirect(url_for('questions'))
    else:
        # User is not in session, so redirect to login
        return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if session.get('user'):
        # Retrieve questions from database
        my_user = db.session.query(User).filter_by(id=session['user_id'])
        my_questions = db.session.query(Question).filter(Question.user_id == session['user_id']).all()
        my_comments = db.session.query(Comment).filter(Comment.user_id == session['user_id']).all()

        return render_template('profile.html', questions=my_questions, comments=my_comments,
                               user_id=my_user, user=session['user'])
    else:
        # Redirect user to login view
        return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/profile', methods=["GET","POST"])
def uploadProfileImage():
    if session.get('user'):
        my_user = db.session.query(User).filter_by(id=session['user_id'])
        my_questions = db.session.query(Question).filter(Question.user_id == session['user_id']).all()
        my_comments = db.session.query(Comment).filter(Comment.user_id == session['user_id']).all()
        
        if request.method == 'POST':
            file = request.files['file']
            if file.filename == '':
                file.filename = 'LDance.gif'
                filename = 'LDance.gif'
            else:
                filename = file.filename
                print(filename)
                print(allowed_file(filename))
                if allowed_file(filename):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                else:
                    flash("Invalid file-type; Please select a file of the following types: jpg, png, or jpeg")
                    return redirect(url_for('profile'))
                
            current_user = User.query.filter_by(id=session['user_id']).first()
            current_user.filename = filename
            db.session.commit()
            
            return render_template('profile.html', questions=my_questions, comments=my_comments, 
                user_id=my_user, user=session['user'])
        else:
            redirect(url_for('profile'))
    else:
        redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        name = request.form['name']
        # create user model
        new_user = User(name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('questions'))

    # Something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()

    # Validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # We know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # User exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # Password match add user info to session
            session['user'] = the_user.name
            session['user_id'] = the_user.id
            # Render view
            return redirect(url_for('questions'))

        # Password check failed
        # Set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # Form did not validate or GET request
        return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    # Check if user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))


@app.route('/questions/<question_id>/comment', methods=['POST'])
def new_comment(question_id):
    if session.get('user'):
        comment_form = CommentForm()
        # Validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # Get comment data
            comment_text = request.form['comment']
            # Get data stamp
            from datetime import date
            today = date.today()
            # Format date mm/dd/yy
            today = today.strftime("%m-%d-%Y")
            # Create new comment
            new_record = Comment(today, comment_text, int(question_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('view_question', question_id=question_id))

    else:
        return redirect(url_for('login'))


@app.route('/questions/<comment_id>/<action>')
def like(comment_id, action):
    if session.get('user'):
        new_like = Like(session['user_id'], int(comment_id))
        new_dislike = Dislike(session['user_id'], int(comment_id))
        if action == 'like':
            db.session.add(new_like)
            db.session.commit()
        if action == 'unlike':
            db.session.delete(Like.query.filter(Like.answer_id==comment_id, Like.user_id==session['user_id']).first())
            db.session.commit()
        if action == 'dislike':
            db.session.add(new_dislike)
            db.session.commit()
        if action == 'undislike':
            db.session.delete(Dislike.query.filter(Dislike.answer_id==comment_id, Dislike.user_id==session['user_id']).first())
            db.session.commit()
        comment = db.session.query(Comment).filter(Comment.id == comment_id).first()
        return redirect(url_for('view_question', question_id=comment.question_id))
    else:
        return redirect(url_for('login'))


@app.route('/reviews')
def reviews():
    if session.get('user'):
        # Retrieve questions from database
        my_review = db.session.query(Review).filter_by(user_id=session['user_id']).all()

        return render_template('reviews.html', reviews=my_review, user=session['user'])
    else:
        return redirect(url_for('reviews'))


@app.route('/new_review', methods=['GET', 'POST'])
def new_review():
    # Check if user is saved in session
    if session.get('user'):
        # Check method used for request
        if request.method == 'POST':
            # Get question detail data
            body = request.form['body']
            # Get data stamp
            from datetime import date
            today = date.today()
            # Format date mm/dd/yyy
            today = today.strftime("%m-%d-%Y")
            # Create new question
            new_rev = Review(body, today, session['user_id'])
            db.session.add(new_rev)
            db.session.commit()

            return redirect(url_for('reviews'))
        else:
            # GET request - show new review form
            return render_template('new_review.html', user=session['user'])
    else:
        # User is not in session, so redirect to login
        return redirect(url_for('reviews'))


@app.route('/delete/<review_id>', methods=['POST'])
def delete_review(review_id):
    # Check if a user is saved in session
    if session.get('user'):
        # Retrieve question from database
        my_review = db.session.query(Review).filter_by(id=review_id).one()

        db.session.delete(my_review)
        db.session.commit()

        return redirect(url_for('reviews'))
    else:
        # User is not in session, so redirect to login
        return redirect(url_for('reviews'))


@app.route('/reviews/edit/<review_id>', methods=['GET', 'POST'])
def update_review(review_id):
    # Check if user is saved in session
    if session.get('user'):
        # Check method used for request
        if request.method == 'POST':
            # Get question data
            header = request.form['header']
            body = request.form['body']

            review = db.session.query(Review).filter_by(id=review_id).one()

            # Update question data
            review.header = header
            review.body = body
            # Update note in db
            db.session.add(review)
            db.session.commit()

            return redirect(url_for('reviews'))
        else:
            # GET request - show new question form to edit question details
            # Retrieve user from database
            my_review = db.session.query(Question).filter_by(id=review_id).one()

            return render_template('new_question.html', review=my_review, user=session['user'])


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.query.data
        results = db.query.all()
        return render_template('search.html', form=form, results=results)

    return render_template('search.html', form=form)


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000
