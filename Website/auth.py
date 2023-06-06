#For authentication


from flask import Blueprint, render_template, request, flash, redirect, url_for
#from .database import User
from werkzeug.security import generate_password_hash, check_password_hash
# from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login',  methods=['GET', 'POST'])
def login():
    # data = request.form 
    # print(data)
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return render_template("home.html")

@auth.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2') 
        
        #To make sure the user details is valid
        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category="error")
        elif len(name) < 2:
            flash('Name must be greater than 2 characters.', category="error")
        elif password1 != password2:
            flash('Passwords do not match.', category="error")
        elif len(password1) < 6:
            flash('Password must be greater than 6 characters.', category="error")
        else:
            #Add user to database
            flash('Account created succesfully.', category="success")
    
    return render_template("sign_up.html")


@auth.route('/companylogin',  methods=['GET', 'POST'])
def companylogin():
    data = request.form 
    print(data)
    return render_template("companylogin.html")


@auth.route('/companysign-up',  methods=['GET', 'POST'])
def companysign_up():
    if request.method == 'POST':
        companyemail = request.form.get('companyemail')
        companyname = request.form.get('companyname')
        companypassword1 = request.form.get('companypassword1')
        companypassword2 = request.form.get('companypassword2') 
        
        #To make sure the user details is valid
        if len(companyemail) < 4:
            flash('Email must be greater than 4 characters.', category="error")
        elif companypassword1 != companypassword2:
            flash('Passwords do not match.', category="error")
        elif len(companypassword1) < 6:
            flash('Password must be greater than 6 characters.', category="error")
        else:
            #Add user to database
            # new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            # db.session.add(new_user)
            # db.session.commit()
            flash('Account created succesfully.', category="success")
            return redirect(url_for('views.home'))
    
    return render_template("companysign_up.html")