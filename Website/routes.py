from Website import app, db, login_manager
from flask import render_template,redirect, url_for, flash, request, send_file, make_response
from Website.forms import Companyloginform, Companysignupform, Userloginform,Usersignupform,Jobforms
from Website.models import User, Company, Upload, Upload1, Companydash, Companydashb
from flask_login import  login_user, logout_user,current_user,login_required
from io import BytesIO
import os
from flask_sqlalchemy import SQLAlchemy

#Homepage
@app.route("/")
@app.route('/home')
def home():
    # connection = mysql.connector.connect(
    #     host=app.config['MYSQL_HOST'],
    #     user=app.config['MYSQL_USER'],
    #     password=app.config['MYSQL_PASSWORD'],
    #     database=app.config['MYSQL_DB']
    # )
    return render_template('home.html', title='Home')


#Jobs page in homepage
@app.route('/jobs')
def jobs():
    data = Companydashb.query.all()
    
    
    job=[]
    for item in data:
        item_dict ={
            'compname' : item.compname,
            'location': item.location,
            'sector': item.sector,
            'period': item.service_period,
            'category': item.category,
            'job_description': item.job_description
        }
        job.append(item_dict)
    return render_template('jobs.html', title='Available Jobs', data=data)


    


#User login route
@app.route('/userlogin', methods=['POST', 'GET'])
def userlogin():
    if current_user.is_authenticated:
        return redirect(url_for('apply_for_jobs'))
    form=Userloginform()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and form.password.data==user.password:
            login_user(user)
            return redirect(url_for('apply_for_jobs'))
        else:
            flash('Login unsuccessful', category='danger')
    #flash('Login unsuccessful', category='danger')    
    return render_template('userlogin.html', title='User Login', form=form)


#user signup route
@app.route('/usersignup', methods=['POST', 'GET'])
def usersignup():
    form=Usersignupform()
    if form.validate_on_submit():
        user=User(name=form.name.data,email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. Please Login', category='success')
        return redirect(url_for('userlogin'))
    return render_template('usersignup.html', title='New User Sign Up', form=form)
    

#user list of available jobs page
@app.route('/apply_for_jobs')
@login_required
def apply_for_jobs():
    data = Companydashb.query.all()
    
    
    job=[]
    for item in data:
        item_dict ={
            'compname' : item.compname,
            'location': item.location,
            'sector': item.sector,
            'period': item.service_period,
            'category': item.category,
            'job_description': item.job_description
        }
        job.append(item_dict)
    return render_template('apply_for_jobs.html', title='Available Jobs', data=data)


#User dashboard route that allows User upload CV
@app.route('/userdashboard', methods=['POST', 'GET'])
@login_required
def userdashboard():
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    
    
    if request.method == "POST":
        file = request.files['file']
        
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)          
        db.session.commit()
        flash('CV uploaded successfully', category='success') 
        return redirect(url_for('userdashboardform'))
    else:
        return render_template('userdashboard.html', title='Dashboard')
        
    return render_template('userdashboard.html', title='Dashboard')


# User dashboard form
@app.route('/userdashboardform', methods=['POST', 'GET'])
@login_required
def userdashboardform():   
    
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    if request.method == "POST":    
        location = request.form.get('location')
        service_period = request.form.get('service_period')
        sector = request.form.get('service')
        category = request.form.get('category')

        upload1 = Upload1(location=location, service_period=service_period, sector=sector, category=category )
        db.session.add(upload1)         
        db.session.commit()
        flash('Uploaded successfully', category='success') 
    else:
        return render_template('userdashboardform.html', title='Dashboard')
    return render_template('userdashboardform.html', title='Dashboard')


#route to download the data
@app.route('/download/<upload_id>')
def download(upload_id):
    cvs = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(cvs.data), attachment_filename=cvs.filename, as_attachment=True)

document_directory = 'c:\\Users\\UC\\Desktop\\ITMWebApp\\web_flask\\uploads'

#Route to download CV
@app.route('/cvs/<int:id>')
def show_uploaded_cv(id):  # sourcery skip: use-named-expression
    cv = Upload.query.get(id)
    #if cv:
     #   return send_file(BytesIO(cv.data), attachment_filename=Upload.filename, as_attachment=False)
    #else:
     #   return render_template('cvs.html', document=cv)
    if cv is None:
        return 'Document not found'
    filename = cv.filename
    filepath = os.path.join(document_directory, filename)
    return send_file(BytesIO(cv.data))
    

#company login route
@app.route('/companylogin', methods=['POST', 'GET'])
def companylogin():
    if current_user.is_authenticated:
        return redirect(url_for('companydashboard'))
    form=Companyloginform()
    if form.validate_on_submit():
        company=Company.query.filter_by(email=form.email.data).first()
        if company and form.password.data==company.password:
            login_user(company)
            return redirect(url_for('companydashboard'))
        else:
            flash('Login unsuccessful', category='danger')
    return render_template('companylogin.html', title='Company Login', form=form)

#company signup route
@app.route('/companysignup', methods=['POST', 'GET'])
def companysignup():
    
    form=Companysignupform()
    if form.validate_on_submit():
        company=Company(name=form.name.data,email=form.email.data, password=form.password.data)
        db.session.add(company)
        db.session.commit()
        flash('Account created successfully. Please Login', category='success')
        return redirect(url_for('companylogin'))
    return render_template('companysignup.html', title='New Company Sign Up', form=form)


#company dashboard route
@app.route('/companydashboard', methods=['POST', 'GET'])
@login_required
def companydashboard():
    

    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    if request.method == 'POST':
        
        compname = request.form.get('compname')
        location = request.form.get('location')
        service_period = request.form.get('service_period')
        sector = request.form.get('sector')
        category = request.form.get('category')
        job_description = request.form.get('job_description')

        companydashb = Companydashb(compname=compname,location=location, service_period=service_period, sector=sector, category=category, job_description=job_description )
        db.session.add(companydashb)         
        db.session.commit()
        flash('Posted successfully', category='success') 
    else:
        return render_template('companydashboard.html', title='Dashboard')
    return render_template('companydashboard.html', title='Dashboard')


#logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))