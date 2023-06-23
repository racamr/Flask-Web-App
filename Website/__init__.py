from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
import secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)

app.config['MONGO_URI'] = "mongodb+srv://rachelamruthaluri2:gD2ljliEiPLCOY5F@racamrger.d0qawht.mongodb.net/Matchmaker?retryWrites=true&w=majority"

# Initialize the MongoDB database
mongo = PyMongo(app)

# Flask Login Manager
login_manager = LoginManager(app)
login_manager.init_app(app)
