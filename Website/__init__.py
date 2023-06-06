

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
Database_Name = "database.db"


def create_app():
        app = Flask(__name__)
        app.config['SECRET KEY'] = 'secret key'
        app.secret_key = 'secret key'
        
        #database location
        #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Database_Name}'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/User'
        #initialize database
        db.init_app(app)
    
    
        #registering blueprints
        from .views import views
        from .auth import auth
        
        #Registering blueprints
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        
        #from .database import User
        
        #create_database(app)

        return app

def create_database(app):
        if not path.exists(f'Website/{Database_Name}'):
                db.create_all(app=app)
                print('Database created')
    
