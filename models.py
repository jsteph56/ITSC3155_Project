from database import db


class Question(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    header = db.Column("header", db.String(300))
    body = db.Column("body", db.String(10000))
    date = db.Column("date", db.String(50))
    likes = db.Column("likes", db.Integer)
    dislikes = db.Column("dislikes", db.Integer)
    topics = db.Column("topics", db.String(10))
    # imageURL = db.Column("imageURL", db.String(500)) - implement later

    def __init__(self, header, body, topics):
        self.header = header
        self.body = body
        self.likes = 0
        self.dislikes = 0
        self.topics = topics
        # self.imageURL = imageURL


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(50))

    def __init(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
