from database import db
import datetime


class Question(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    header = db.Column("header", db.String(300))
    body = db.Column("body", db.String(10000))
    date = db.Column("date", db.String(50))
    topics = db.Column("topics", db.String(10))
    filename = db.Column("filename", db.String(150), nullable=False, server_default='aardvark_logo.png')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="question", cascade="all, delete-orphan", lazy=True)

    def __init__(self, header, body, date, topics, user_id):
        self.header = header
        self.body = body
        self.date = date
        self.topics = topics
        # self.imageURL = imageURL
        self.user_id = user_id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column("date", db.String(50))
    content = db.Column(db.VARCHAR, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    likes = db.relationship("Like", backref="comment", lazy="dynamic")

    def __init__(self, date, content, question_id, user_id):
        self.date = date
        self.content = content
        self.question_id = question_id
        self.user_id = user_id


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(50), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    questions = db.relationship("Question", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    filename = db.Column("filename", db.String(150), nullable=False, server_default='aardvark_logo.png')
    liked = db.relationship("Like", foreign_keys="Like.user_id", backref="user", lazy='dynamic')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()

    def like_answer(self, answer):
        if not self.liked_answer(answer):
            like = Like(user_id=self.id, answer_id="comment.id")
            db.session.add(like)
            self.likes += 1

    def unlike_answer(self, answer):
        if self.liked_answer(answer):
            Like.query.filter_by(user_id=self.id, answer_id="comment.id").delete()
            self.likes -= 1

    def liked_answer(self, answer):
        return Like.query.filter(Like.user_id == self.id, Like.answer_id == "comment.id").count() > 0

    def num_of_likes(self):
        return self.likes.count()


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, answer_id, user_id):
        self.answer_id = answer_id
        self.user_id = user_id


class Review(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    body = db.Column("body", db.String(10000))
    date = db.Column("date", db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, body, date, user_id):
        self.body = body
        self.date = date
        self.user_id = user_id
