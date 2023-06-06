import tempfile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine
from flask_login import LoginManager
from datetime import datetime

from os import path
from Website import routes



def create_app():
        app = Flask(__name__)
        app.config['SECRET KEY'] = 'secret key'
        app.secret_key = 'secret key'
        
        #database location
        
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/User'
        #initialize database
        db.init_app(app)

        return app

app = Flask(__name__)

db=SQLAlchemy(app)
app.app_context().push()

with app.app_context():
    db.create_all()

#Flask login Manager
login_manager = LoginManager(app)
login_manager.init_app(app)




    
