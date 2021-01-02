from datetime import datetime
from flask import redirect, url_for, flash, current_app
from flask_blogg import db, login_manager
from flask_login import UserMixin
from hashlib import md5
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, Admin
from flask_login import current_user
from flask_blogg import admin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.now)
    about_me = db.Column(db.String(200), nullable=True)
    usertype = db.Column(db.Integer, nullable=True)
    approved = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='author',  lazy=True)
    pastes = db.relationship('Paste', backref='author', lazy=True)
    dailyrecord = db.relationship('dailyRecord',backref='author',lazy=True)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_reset_token(self, expire_secs=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_secs)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"{self.username} , {self.email}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"The post is {self.title} on {self.date_posted}"

class dailyRecord(db.Model):
    __tablename__="dailyrecord"
    id = db.Column(db.Integer, primary_key=True)
    morningwalk = db.Column(db.Boolean, nullable=False)
    waterdrank = db.Column(db.Integer,nullable=False)
    breakfast = db.Column(db.Boolean,nullable=False)
    breakfast_calories=db.Column(db.Integer, nullable=False)
    lunch = db.Column(db.Boolean,nullable=False)
    lunch_calories=db.Column(db.Integer, nullable=False)
    dinner = db.Column(db.Boolean,nullable=False)
    dinner_calories=db.Column(db.Integer, nullable=False)
    total_calories = db.Column(db.Integer,nullable=False)
    nightwalk = db.Column(db.Boolean,nullable=False)
    comment = db.Column(db.Text,nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    posted_or_not = db.Column(db.Integer,nullable=False,default=0)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'This is the daily record'

    @property
    def serialize(self):
        return {'name': self.id or 'Null',
                'morningwalk':self.morningwalk or 'Null',
                'waterdrank':self.waterdrank or 'Null',
                'breakfast':self.breakfast or 'Null',
                'breakfast_calories':self.breakfast_calories or 'Null',
                'lunch':self.lunch or 'Null',
                'lunch_calories':self.lunch_calories or 'Null',
                'dinner':self.dinner or 'Null',
                'dinner_calories':self.dinner_calories or 'Null',
                'total_calories':self.total_calories or 'Null',
                'nightwalk':self.nightwalk or 'Null',
                'comment':self.comment or 'Null'
                }

class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'The id of the paste is {self.id}'


class MyModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_anonymous:
            if current_user.email == 'janakisasidhar1@gmail.com':
                return True
            else:
                return False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        flash('You dont have rights to access this page', 'danger')
        return redirect(url_for('users.login'))


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
