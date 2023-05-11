#
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'secret key'
    app.secret_key = 'secret key'
    
    #registering blueprints
    from .views import views
    from .auth import auth
    
    #Registering blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
