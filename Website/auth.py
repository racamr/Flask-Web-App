#For authentication


from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login',  methods=['GET', 'POST'])
def login():
    data = request.form 
    print(data)
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