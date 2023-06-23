from flask import Flask, render_template, flash, redirect, url_for, request, send_file
from flask_pymongo import ObjectId
from flask_login import login_user, logout_user, current_user, login_required
from io import BytesIO
import os
from Website.forms import Companyloginform, Companysignupform, Userloginform, Usersignupform, Jobforms
from Website.models import User, Company, Upload, Upload1, Companydashb
from Website import app, mongo, login_manager

# Homepage
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

# Jobs page in homepage
@app.route('/jobs')
def jobs():
    data = mongo.db.Matchmaker.Companydashb.find()
    result = []
    for document in data:
        result.append({
            'compname': document['compname'],
            'location': document['location'],
            'sector': document['sector'],
            'service_period': document['service_period'],
            'category': document['category'],
            'job_description': document['job_description']
        })
    return render_template('jobs.html', title='Available Jobs', data=data)

# Get the base directory of the Flask app
base_dir = app.root_path

# Create the uploads directory path relative to the base directory
document_directory = os.path.join(base_dir, 'uploads')

# User login route
@app.route('/userlogin', methods=['POST', 'GET'])
def userlogin():
    if current_user.is_authenticated:
        return redirect(url_for('apply_for_jobs'))
    form = Userloginform()
    if form.validate_on_submit():
        user = mongo.db.Matchmaker.users.find_one({'email': form.email.data})
        if user and form.password.data == user['password']:
            login_user(user)
            return redirect(url_for('apply_for_jobs'))
        else:
            flash('Login unsuccessful', category='danger')
    return render_template('userlogin.html', title='User Login', form=form)

# User signup route
@app.route('/usersignup', methods=['POST', 'GET'])
def usersignup():
    form = Usersignupform()
    if form.validate_on_submit():
        user = {
            'name': form.name.data,
            'email': form.email.data,
            'password': form.password.data
        }
        mongo.db.Matchmaker.users.insert_one(user)
        flash('Account created successfully. Please Login', category='success')
        return redirect(url_for('userlogin'))
    return render_template('usersignup.html', title='New User Sign Up', form=form)

# User list of available jobs page
@app.route('/apply_for_jobs')
@login_required
def apply_for_jobs():
    data = mongo.db.Matchmaker.companydashb.find()
    job = []
    for item in data:
        item_dict = {
            'compname': item['compname'],
            'location': item['location'],
            'sector': item['sector'],
            'period': item['service_period'],
            'category': item['category'],
            'job_description': item['job_description']
        }
        job.append(item_dict)
    return render_template('apply_for_jobs.html', title='Available Jobs', data=job)

# User dashboard route that allows User to upload CV
@app.route('/userdashboard', methods=['POST', 'GET'])
@login_required
def userdashboard():
    if request.method == "POST":
        file = request.files['file']
        upload = {
            'filename': file.filename,
            'data': file.read()
        }
        mongo.db.Matchmaker.uploads.insert_one(upload)
        flash('CV uploaded successfully', category='success')
        return redirect(url_for('userdashboardform'))
    return render_template('userdashboard.html', title='Dashboard')

# User dashboard form
@app.route('/userdashboardform', methods=['POST', 'GET'])
@login_required
def userdashboardform():
    if request.method == "POST":
        location = request.form.get('location')
        service_period = request.form.get('service_period')
        sector = request.form.get('service')
        category = request.form.get('category')
        upload1 = {
            'location': location,
            'service_period': service_period,
            'sector': sector,
            'category': category
        }
        mongo.db.Matchmaker.upload1s.insert_one(upload1)
        flash('Uploaded successfully', category='success')
    return render_template('userdashboardform.html', title='Dashboard')

# Route to download the data
@app.route('/download/<upload_id>')
def download(upload_id):
    cvs = mongo.db.Matchmaker.uploads.find_one({'_id': ObjectId(upload_id)})
    return send_file(BytesIO(cvs['data']), attachment_filename=cvs['filename'], as_attachment=True)

# Route to download CV
@app.route('/cvs/<int:id>')
def show_uploaded_cv(id):
    cv = mongo.db.Matchmaker.uploads.find_one({'_id': ObjectId(id)})
    if cv is None:
        return 'Document not found'
    filename = cv['filename']
    filepath = os.path.join(document_directory, filename)
    return send_file(BytesIO(cv['data']))

# Company login route
@app.route('/companylogin', methods=['POST', 'GET'])
def companylogin():
    if current_user.is_authenticated:
        return redirect(url_for('companydashboard'))
    form = Companyloginform()
    if form.validate_on_submit():
        company = mongo.db.Matchmaker.companies.find_one({'email': form.email.data})
        if company and form.password.data == company['password']:
            login_user(company)
            return redirect(url_for('companydashboard'))
        else:
            flash('Login unsuccessful', category='danger')
    return render_template('companylogin.html', title='Company Login', form=form)

# Company signup route
@app.route('/companysignup', methods=['POST', 'GET'])
def companysignup():
    form = Companysignupform()
    if form.validate_on_submit():
        company = {
            'name': form.name.data,
            'email': form.email.data,
            'password': form.password.data
        }
        mongo.db.Matchmaker.companies.insert_one(company)
        flash('Account created successfully. Please Login', category='success')
        return redirect(url_for('companylogin'))
    return render_template('companysignup.html', title='New Company Sign Up', form=form)

# Company dashboard route
@app.route('/companydashboard', methods=['POST', 'GET'])
@login_required
def companydashboard():
    if request.method == 'POST':
        compname = request.form.get('compname')
        location = request.form.get('location')
        service_period = request.form.get('service_period')
        sector = request.form.get('sector')
        category = request.form.get('category')
        job_description = request.form.get('job_description')
        companydashb = {
            'compname': compname,
            'location': location,
            'service_period': service_period,
            'sector': sector,
            'category': category,
            'job_description': job_description
        }
        mongo.db.Matchmaker.companydashb.insert_one(companydashb)
        flash('Posted successfully', category='success')
    return render_template('companydashboard.html', title='Dashboard')

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)