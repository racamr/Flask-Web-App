from flask import Flask, render_template, flash, redirect, url_for, request, send_file
from flask_pymongo import ObjectId
from flask_login import login_user, logout_user, current_user, login_required
from io import BytesIO
import os
from Website.forms import Companyloginform, Companysignupform, Userloginform, Usersignupform, Jobforms
from Website.models import User, Company, Upload, Upload1, Companydashb
from Website import app, mongo, login_manager
import random
import stripe

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


#Stripe Payment
stripe.api_key = 'sk_test_51NMnCbFYkG4STZrMg8isctViW38wCtJOdg9ZM19oUfhwF1Y1h8kkWvqq9HKDZcTp50flokYeIr6znlqtq0zlCiXF00QmNXMNyw'

public_key = "pk_test_51NMnCbFYkG4STZrMKNIU7s4TKifXochk0KmITYtC7jB2dIjaEwmnD4hXtQ7HOfpKwVSy5fmt3Bw6lHCwZnaUeL3X00hwWlCtYr"

#User payment
@app.route("/payment")
def payment():
    return render_template("payment.html", public_key=public_key, title='Payment')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/paynow', methods=['POST'])
def paynow():
    
    #customer
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    
    #payment info
    charge = stripe.Charge.create(
        customer=customer.id, 
        amount=2500,
        currency='eur',
        description='SignUp Fee'
    )
    return render_template('thankyou.html')


#Company payment
@app.route("/companypayment")
def companypayment():
    return render_template("companypayment.html", public_key=public_key, title='Payment')

@app.route('/companythankyou')
def companythankyou():
    return render_template('companythankyou.html')

@app.route('/companypaynow', methods=['POST'])
def companypaynow():
    
    #customer
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    
    #payment info
    charge = stripe.Charge.create(
        customer=customer.id, 
        amount=2500,
        currency='eur',
        description='SignUp Fee'
    )
    return render_template('companythankyou.html')



# Responses provided by the chatbot
chatbot_responses = {
    'greeting': ['Hello! How can I assist you with your job search?', 'Hi! How may I help you with your job search?'],
    'job_openings': ['We have several job openings in different fields. Could you please specify your preferred job role?', 'Sure! What kind of job are you looking for?'],
    'guide': ['Sure! I can help you navigate through the app. What would you like assistance with?', 'How can I assist you in navigating through the app?'],
    'thanks': ['Sure! anytime you"re Welcome'],
    
}


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    response = get_chatbot_response(user_message)
    return response

def get_chatbot_response(user_message):

    user_message = user_message.lower()

    # Rule-based matching for different user intents
    if any(keyword in user_message for keyword in ['hello', 'hi', 'hey']):
        return random.choice(['Hello! How can I assist you with your job search?', 'Hi! How may I help you with your job search?'])
    elif any(keyword in user_message for keyword in ['job', 'opening']):
        return random.choice(['We have several job openings in different fields. Could you please specify your preferred job role?', 'Sure! What kind of job are you looking for?'])
    elif any(keyword in user_message for keyword in ['guide', 'help']):
        return random.choice(['Sure! I can help you navigate through the app. What would you like assistance with?', 'How can I assist you in navigating through the app?'])
    elif any(keyword in user_message for keyword in ['resume', 'cv']):
        return random.choice(['To create a resume, you can use our built-in resume builder tool or upload your existing resume. Which option would you like to choose?', 'We offer a resume creation feature. Would you like to build a resume from scratch or upload an existing one?'])
    elif any(keyword in user_message for keyword in ['interview', 'prepare']):
        return random.choice(['Preparing for an interview is crucial. We provide interview tips and commonly asked questions for various job roles. How can I assist you specifically?', 'Interview preparation is important. Let me know what kind of assistance you need for your interview.'])
    elif any(keyword in user_message for keyword in ['salary', 'pay']):
        return random.choice(['Salary ranges vary depending on the job and location. Could you please provide more information about the job you are interested in?', 'Salary information is job-specific. Let me know the job title, and I can provide you with an estimated salary range.'])
    elif any(keyword in user_message for keyword in ['remote', 'work from home']):
        return random.choice(['Yes, we have remote job opportunities available. What kind of remote job are you looking for?', 'Remote work is becoming increasingly popular. Could you specify the job field in which you are interested?'])
    elif any(keyword in user_message for keyword in ['skills', 'improve']):
        return random.choice(['Improving your skills is crucial for career growth. Which skills do you want to focus on?', 'Continuous skill improvement is important. Let me know the skills you want to enhance.'])
    elif any(keyword in user_message for keyword in ['application', 'status']):
        return random.choice(['To check the status of your application, please provide the application ID or the email address used during the application process.', 'To provide the application status, I need your application ID or the email address you used during the application.'])
    elif any(keyword in user_message for keyword in ['company', 'information']):
        return random.choice(['We have information on various companies. Please provide the name of the company you want information about.', 'Sure, I can provide information about different companies. Let me know the name of the company.'])
    elif any(keyword in user_message for keyword in ['training', 'courses']):
        return random.choice(['We offer a wide range of training courses to enhance your skills. What specific training are you interested in?', 'Training and courses are available for various skills. Let me know the skill you want to focus on.'])
    elif any(keyword in user_message for keyword in ['internship', 'intern']):
        return random.choice(['Internship opportunities are available in different fields. Can you please provide your area of interest for the internship?', 'Sure! What type of internship are you looking for?'])
    elif any(keyword in user_message for keyword in ['job fair', 'career fair']):
        return random.choice(['We organize job fairs regularly. Is there any specific job fair you want information about?', 'Job fairs are a great opportunity to connect with employers. Let me know the location or date for the job fair you are interested in.'])
    elif any(keyword in user_message for keyword in ['networking', 'connect']):
        return random.choice(['Networking is important for career growth. Are you looking for networking events or online networking platforms?', 'Networking can help you expand your professional connections. Let me know the type of networking you are interested in.'])
    elif any(keyword in user_message for keyword in ['interview tips', 'interview question']):
        return random.choice(['We provide interview tips and commonly asked questions for various job roles. Let me know the job role you want interview tips for.', 'Interview tips and questions are available for different job roles. Can you please specify the job role?'])
    elif any(keyword in user_message for keyword in ['job search', 'find job']):
        return random.choice(['Job search can be overwhelming. Let me know the specific job role and location you are looking for.', 'I can assist you in finding a job. Please provide the job role and location you are interested in.'])
    elif any(keyword in user_message for keyword in ['company culture', 'work environment']):
        return random.choice(['Company culture and work environment vary. Can you provide the name of the company you want information about?', 'Sure, I can provide information about the company culture and work environment. Please provide the name of the company.'])
    elif any(keyword in user_message for keyword in ['career change', 'switch careers']):
        return random.choice(['Switching careers requires careful planning. Can you please provide more information about your current and desired career paths?', 'Career change can be a significant decision. Let me know your current and desired career paths for better guidance.'])
    elif any(keyword in user_message for keyword in ['job description', 'responsibilities']):
        return random.choice(['Job descriptions provide an overview of job roles and responsibilities. Please specify the job title for which you want the description.', 'Sure, I can provide job descriptions. Let me know the job title you are interested in.'])
    elif any(keyword in user_message for keyword in ['career advice', 'guidance']):
        return random.choice(['Career advice can help you make informed decisions. Can you please provide more details about the specific aspect you need advice on?', 'I can provide career guidance. Let me know the area you need assistance with.'])
    elif any(keyword in user_message for keyword in ['work-life balance', 'well-being']):
        return random.choice(['Work-life balance is important for overall well-being. How can I assist you in maintaining a healthy work-life balance?', 'Sure, work-life balance is crucial. Let me know the specific area you need assistance with.'])
    elif any(keyword in user_message for keyword in ['job application', 'apply']):
        return random.choice(['To apply for a job, visit our website and navigate to the "Careers" section. You can find job listings and application instructions there.', 'You can apply for a job through our website. Please visit the "Careers" section for job listings and application details.'])
    elif any(keyword in user_message for keyword in ['career growth', 'advancement']):
        return random.choice(['Career growth is important for professional advancement. Let me know the specific area you want to focus on for your career growth.', 'Sure, career growth is crucial. How can I assist you in advancing your career?'])
    elif any(keyword in user_message for keyword in ['workplace diversity', 'inclusion']):
        return random.choice(['Workplace diversity and inclusion are significant. How can I assist you in understanding and promoting diversity and inclusion in the workplace?', 'Sure, workplace diversity and inclusion are important. Let me know the specific area you need assistance with.'])
    elif any(keyword in user_message for keyword in ['professional development', 'skills enhancement']):
        return random.choice(['Professional development is key for enhancing skills. What specific area or skills do you want to focus on for your professional development?', 'Sure, professional development is important. Let me know the specific area you want to enhance your skills in.'])
    elif any(keyword in user_message for keyword in ['company benefits', 'perks']):
        return random.choice(['Company benefits and perks vary. Can you provide the name of the company you want information about?', 'Sure, I can provide information about company benefits and perks. Please provide the name of the company.'])
    elif any(keyword in user_message for keyword in ['workplace ethics', 'professional conduct']):
        return random.choice(['Workplace ethics and professional conduct are essential. How can I assist you in understanding and promoting workplace ethics?', 'Sure, workplace ethics and professional conduct are important. Let me know the specific area you need assistance with.'])
    elif any(keyword in user_message for keyword in ['job satisfaction', 'career happiness']):
        return random.choice(['Job satisfaction and career happiness are crucial. How can I assist you in finding job satisfaction?', 'Sure, job satisfaction is important. Let me know the specific area you need assistance with.'])
    elif any(keyword in user_message for keyword in ['promotion', 'raise']):
        return random.choice(['Promotions and raises are based on various factors. Can you provide more information about your current job position and the desired promotion or raise?', 'Sure, promotions and raises depend on different factors. Let me know the details about your current job position and the desired promotion or raise.'])
    elif any(keyword in user_message for keyword in ['job search platform', 'website']):
        return random.choice(['We have our own job search platform. Please visit our website and navigate to the "Careers" section for job listings.', 'We offer a job search platform on our website. Visit our website and go to the "Careers" section to find job listings.'])
    elif any(keyword in user_message for keyword in ['remote collaboration', 'virtual teamwork']):
        return random.choice(['Remote collaboration and virtual teamwork have become important. How can I assist you in improving remote collaboration?', 'Sure, remote collaboration and virtual teamwork are crucial. Let me know the specific area you need assistance with.'])
    elif any(keyword in user_message for keyword in ['job market', 'industry trends']):
        return random.choice(['The job market and industry trends vary. Can you provide more information about the specific job market or industry you are interested in?', 'Sure, job market and industry trends are diverse. Let me know the details about the specific job market or industry you want information on.'])
    elif any(keyword in user_message for keyword in ['workplace communication', 'effective communication']):
        return random.choice(['Workplace communication and effective communication skills are important. How can I assist you in improving workplace communication?', 'Sure, workplace communication and effective communication skills are crucial. Let me know the specific area you need assistance with.'])
    elif any(keyword in user_message for keyword in ['job interview', 'interview tips']):
        return random.choice(['Job interviews are crucial. Can you provide more information about the specific job role and the interview stage?', 'Sure, job interviews require preparation. Let me know the details about the specific job role and the interview stage for better guidance.'])
    # Add more rule-based matching below

    # Machine learning responses
    ml_responses = [
        "I'm sorry, I'm still learning and may not have an answer for that yet.",
        "I'm not sure I understand. Can you please provide more information?",
        "That's interesting. Let me think for a moment...",
        "I'm continuously learning and evolving, so I may not have a response for that right now.",
        "I apologize, but I don't have the information you're looking for. Is there anything else I can help with?"
        # Add more machine learning responses here
    ]

    if len(ml_responses) > 0:
        return random.choice(ml_responses)
    else:
        return 'I apologize, but I am not able to assist with that at the moment.'


# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
