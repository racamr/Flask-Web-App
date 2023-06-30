#File contains database models

from Website import mongo, login_manager 
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, LoginManager

from flask import redirect,url_for

#from sqlalchemy.orm import relationship

from flask_pymongo import ObjectId

@login_manager.user_loader
def load_user_person(user_id):
    user_data=mongo.db.Matchmaker.User.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

@login_manager.user_loader
def load_user_company(company_id):
    company_data=mongo.db.Matchmaker.User.find_one({'_id': ObjectId(company_id)})
    if company_data:
        return Company(company_data)
    return None
   
class Upload:
    def _init_(self, user_id, filename, data):
        self.user_id = user_id
        self.filename = filename
        self.data = data

    def _repr_(self):
        return f'{self.filename}'

class Upload1:
    def _init_(self, user_id, location, sector, service_period, category):
        self.user_id = user_id
        self.location = location
        self.sector = sector
        self.service_period = service_period
        self.category = category

    def _repr_(self):
        return f'{self.user_id} : {self.location} : {self.sector} : {self.service_period} : {self.category}'

class Company(UserMixin):
    #def _init_(self, name, email, password, date_created):
    def __init__(self, company_data): 
        self.id = str(company_data['_id']) 
        self.name = company_data['name']
        self.email = company_data['email']
        self.password = company_data['password']
        #self.datetime = company_data['datetime']

    def _repr_(self):
        return f'{self.name} : {self.email} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'

class Companydashb:
    def _init_(self, user_id, compname, location, sector, service_period, category, job_description):
        self.user_id = user_id
        self.compname = compname
        self.location = location
        self.sector = sector
        self.service_period = service_period
        self.category = category
        self.job_description = job_description

    def _repr_(self):
        return f'{self.compname} : {self.location} : {self.sector} : {self.service_period} : {self.category}'
    
    def get_id(self): 
        return self.id 
    
    def is_authenticated(self): 
        return True
    
    def is_active(self): 
        return True
    
    def is_anonymous(self): 
        return False
    
class User(UserMixin): 
    def __init__(self, user_data): 
        self.id = str(user_data['_id']) 
        self.name = user_data['name'] 
        self.email = user_data['email'] 
        self.password = user_data['password'] 
        self.datetime = user_data['datetime']
        # Update relationships 
        # if needed 
       
    def get_id(self): 
        return self.id 
    
    def is_authenticated(self): 
        return True
    
    def is_active(self): 
        return True
    
    def is_anonymous(self): 
        return False
    

# @login_manager.unauthorized_handler
# def unauthorized():
#     return redirect(url_for('home'))

#User database model
"""
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
    companydashb = db.relationship('Companydashb', backref='companydashb')
    
    def __repr__(self):
        return f'{self.name} : {self.email} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'
    
    
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
    
"""
    

    