import uuid
from app import db
from app.config import Config
from datetime import datetime


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.String(36), db.ForeignKey('user.public_id'))

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, title, created_by):
        self.title = title
        self.created_by = created_by

    def __repr___(self):
        return f"Todo({self.title[:80]}-{self.created_by})"


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    public_id = db.Column(
        db.String(36), default=str(uuid.uuid4()), unique=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    profile_pic = db.Column(
        db.String(), default=Config.BASE_URL+'/static/default.png')
    secret_code = db.Column(db.String(8), nullable=True)
    active = db.Column(db.Boolean, default=False)
    todos = db.relationship(Todo, backref='todos', lazy='joined')

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, email, password, first_name=None, last_name=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def __repr___(self):
        return f"User({self.email}-{self.first_name})"
