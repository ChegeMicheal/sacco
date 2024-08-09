from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

    
class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key = True)
    fullName = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique = True, nullable=False)
    password = db.Column(db.String(150))

    #create string
    def __repr__(self):
        return '<Name %r>' % self.name

class Account(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    account_name=db.Column(db.String(150), nullable=False)
    account_number=db.Column(db.String(150), nullable=False)
    debit=db.Column(db.Integer)
    credit=db.Column(db.Integer)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    
class Credit(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    credits=db.Column(db.String(1000), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
