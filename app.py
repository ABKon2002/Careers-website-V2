from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from database import DataOperations
import os
import time

# For integrating log-in / Sign-in pages
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from Authentication import RegisterForm, LoginForm, User


app = Flask(__name__, template_folder="Templates")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
b_crypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'danger')
    return redirect(url_for('login'))

DO = DataOperations()

global data
hosting_url = "https://mycareers-dit2.onrender.com/"

# Jobs = DO.loadJobs()

about_us = [
    "We believe in what people make possible.", 
    "Our mission is to empower every person and every organization on the planet to achieve more.", 
    "We believe technology can and should be a force for good and that meaningful innovation can and will contribute to a brighter world in big and small ways.", 
    "We believe that, when designed with people at the center, AI can extend your capabilities.",
    "As the world continues to respond to COVID-19, we are working to do our part by ensuring the safety of our employees.", 
    "Our mission is to ensure that artificial general intelligence benefits all of humanity.",
    "We are building safe and beneficial AGI, but will also consider our mission fulfilled if our work aids others to achieve this outcome.",
    "We research generative models and how to align them with human values."
]


@app.route("/")
def hello_world():
    Jobs = DO.loadJobs()
    return render_template("home.html", hURL = hosting_url, jobs = Jobs, abtUs = about_us)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    # Create an instance of our Registration Form
    form = RegisterForm()
    # After we submit the form...
    if form.validate_on_submit():
        if form.passkey.data != os.getenv('ADMIN_PASSKEY'):
            flash('Invalid Passkey! Retry', 'danger')
            return redirect(url_for('register'))
        # Create a new user dictionary
        new_user = {}
        # Set the username equal to the form's input
        #form.validate_username(request.form.get('username'))
        new_user['username'] = form.username.data
        # Hash the password using Bcrypt
        hashed_password = b_crypt.generate_password_hash(form.password.data)
        # Set the password equal to the hashed password
        new_user['password'] = hashed_password
        # Call the add_user function to store the user in our database
        DO.add_user(new_user)
        # Flash a message to the user saying that the registration was successful
        flash('Registration successful!', 'success')
        # Wait for 2 seconds before redirecting to the login page
        time.sleep(2)     # Redirects to login after 2 seconds. 
        # Redirect to the login page
        return redirect(url_for('login'))
    else:
        # Flash a message to the user saying that the registration failed
        flash('Registration failed', 'danger')

    # Render the register.html template with the form
    return render_template('Auth/register.html', form = form)

@login_manager.user_loader
def load_user(user_id):
    # Use the user_id to fetch the user from the database
    return User.get_by_id(DO, user_id)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_username = DO.return_existing_username(form.username.data)
        if existing_username:
            id = existing_username[0]
            username = existing_username[1]
            password = existing_username[2]
            if b_crypt.check_password_hash(password, form.password.data):
                login_user(User(id, username, password))
                return redirect(url_for('admin_dashboard'))
    return render_template('Auth/login.html', form = form)

@app.route("/jobs")
def show_jobs():
    jobs = DO.loadJobs(query='select * from jobs')
    return render_template('Job/Jobs.html', jobs = jobs)

@app.route("/logout", methods = ['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/api/jobs")    # api-endpoint 1.0: Returns job details as json
def job_details():
    Jobs = DO.loadJobs()
    for i in range(len(Jobs)):
        Jobs[i] = dict(Jobs[i])
    return jsonify(Jobs)

@app.route("/job/<ID>")
def get_job_by_ID(ID):
    Job = DO.loadJob(ID)
    if Job:
        # Splitting the requirements and responsibilities...
        Job = dict(Job)
        if Job["Requirements"]:
            Job['Requirements'] = Job['Requirements'].split('.')
            Job["Requirements"].pop(-1)
        
        if Job['Responsibilities']:
            Job['Responsibilities'] = Job['Responsibilities'].split('.')
            Job["Responsibilities"].pop(-1)
        
        return render_template("Applicant View/1_Job_Page.html", job = Job)
    else:
        return f"No Job entry found under {ID} :(", 404

@app.route("/job/<ID>/apply", methods = ['GET','POST'])
def apply_job(ID):
    job = DO.loadJob(ID)
    if job:
        return render_template('Applicant View/2_applicationForm.html', job = job)
    else:
        return "Job post expired"

@app.route("/job/<ID>/review", methods = ['GET', 'POST'])
def application_submitted(ID):
    global data               # Because of this, this application is not meant for multiple access. 
    data = request.form
    data = dict(data)
    data['techStack'] = request.form.getlist('techStack')
    return render_template('Applicant View/3_reviewApplication.html', data = data, ID = ID)

@app.route("/job/<ID>/confirm", methods = ['POST'])
def confirm_submission(ID):
    global data
    DO.add_application_to_DB(ID, data)
    return render_template('Applicant View/4_applicationSuccess.html', ID = ID)

@app.route("/admin")
@login_required
def admin_dashboard():
    return render_template('Admin View/0_adminDashboard.html')

@app.route("/applications")
@login_required
def view_applications():
    JobList = DO.applications_by_job()
    return render_template('Admin View/1_Applicationview.html', applications_by_job = JobList)

@app.route("/applicant/<app_ID>/review")
@login_required
def review_applicant(app_ID):
    application = DO.loadApplication(app_ID)
    application = dict(application)
    if application['Tech_stack']:
        application['Tech_stack'] = list(application['Tech_stack'].split('. '))
    return render_template('Admin View/1.1_ApplicantDetails.html', application = application)

@app.route("/add/job")
@login_required
def add_job_form():
    return render_template('Admin View/2_AddJob.html')

@app.route("/admin/add_job", methods = ['POST'])
@login_required
def add_job():
    data = request.form
    data = dict(data)
    DO.add_job(data)
    return render_template('Admin View/2.1_JobEntrySuccess.html')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)
