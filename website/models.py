from main import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#database for Note
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    body = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now) #getting current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key, store id of user
    #references User class and id child

#database for User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) #'150' is the length of string, 'unique=True' means only one user can have email
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    note = db.relationship('Note')


#models important for databases