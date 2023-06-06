#File contains database models

from Website import db, login_manager 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

from flask import redirect,url_for

from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    return Company.query.get(user_id)

# @login_manager.unauthorized_handler
# def unauthorized():
#     return redirect(url_for('home'))

#User database model
class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False ) 
    email=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow())
    upload = db.relationship('Upload', backref='upload')
    upload1 = db.relationship('Upload1', backref='upload1')
    
    def __repr__(self):
        return f'{self.name} : {self.email} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'
 
# Model for CV from user    
class Upload(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    filename=db.Column(db.String(100))
    data=db.Column(db.LargeBinary)
    
    # # userid= relationship('User', foreign_keys=['Upload'])
    
    def __repr__(self):
        return f'{self.filename}'
    
# Model for User's forms  
class Upload1(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    location=db.Column(db.String(100))
    sector=db.Column(db.String(30))
    service_period=db.Column(db.String(30))
    category=db.Column(db.String(20))
    
    def __repr__(self):
        return f' {self.user_id} : {self.location} : {self.sector} : {self.service_period} : {self.category}'    
        
# Model for Company Signup form        
class Company(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False ) 
    email=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow())
    companydash = db.relationship('Companydash', backref='companydash')
    companydashb = db.relationship('Companydashb', backref='companydashb')
    
    def __repr__(self):
        return f'{self.name} : {self.email} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'
    

# Model for Company form  (not in use)  
class Companydash(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('company.id'))
    location=db.Column(db.String(100))
    sector=db.Column(db.String(30))
    service_period=db.Column(db.String(30))
    category=db.Column(db.String(20))
    job_description=db.Column(db.String(4000))
    
    def __repr__(self):
        return f' {self.location} : {self.sector} : {self.service_period} : {self.category}' 
    
# Model for Company form     
class Companydashb(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('company.id'))
    compname=db.Column(db.String(100))
    location=db.Column(db.String(100))
    sector=db.Column(db.String(30))
    service_period=db.Column(db.String(30))
    category=db.Column(db.String(20))
    job_description=db.Column(db.String(4000))
    
    def __repr__(self):
        return f' {self.compname} : {self.location} : {self.sector} : {self.service_period} : {self.category}' 
    
    

    