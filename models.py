from database import db
import datetime

class Question(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    header = db.Column("header", db.String(300))
    body = db.Column("body", db.String(10000))
    date = db.Column("date", db.String(50))
    topics = db.Column("topics", db.String(10))
    # imageURL = db.Column("imageURL", db.String(500)) - implement later
    #Can create a foreign key
    #Referencing the id variable in the User class, which is why it is a lowercase u
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="question", cascade="all, delete-orphan", lazy=True)

    def __init__(self, header, body, date, topics, user_id):
        self.header = header
        self.body = body
        self.date = date

        self.topics = topics
        # self.imageURL = imageURL
        self.user_id = user_id


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(50), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    questions = db.relationship("Question", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    liked = db.relationship("Like", foreign_keys="Like.user_id", backref="user", lazy='dynamic')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()

class Like(db.Model):
    __tablename__ = "like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column("date", db.String(50))
    content = db.Column(db.VARCHAR, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    likes = db.Column("likes", db.Integer)
    dislikes = db.Column("dislikes", db.Integer)

    def __init__(self, date, content, question_id, user_id):
        self.date = date
        self.content = content
        self.question_id = question_id
        self.user_id = user_id
        self.likes = 0
        self.dislikes = 0

    def like_question(self, question):
        if not self.liked_question(question):
            like = Like(user_id=self.user_id, answer_id=self.id)
            db.session.add(like)
            self.likes += 1

    def unlike_question(self, question):
        if self.liked_question(question):
            Like.query.filter_by(user_id=self.user_id, answer_id=self.id).delete()
            self.likes -= 1

    def liked_question(self, question):
        return Like.query.filter(Like.user_id == self.user_id, Like.answer_id == self.id).count() > 0


class Review(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    body = db.Column("body", db.String(10000))
    date = db.Column("date", db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, body, date, user_id):
        self.body = body
        self.date = date
        self.user_id = user_id

class ProfilePicture(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    filename = db.Column("filename", db.String(150), nullable=False, profile_default='aardvark_logo.png')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, user_id, filename):
        self.user_id = user_id;
        self.filename = filename;
