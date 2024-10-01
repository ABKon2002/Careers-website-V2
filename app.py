
from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import aiven_engine, loadJobs, loadJob, add_application_to_DB, check_username, add_user, return_existing_username
from sqlalchemy import text
import os
import time

# For integrating log-in / Sign-in pages
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__, template_folder="Templates")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
b_crypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

global data
hosting_url = "https://mycareers-2nex.onrender.com"

Jobs = loadJobs(aiven_engine)

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

class LoginForm(FlaskForm):
    username = StringField(validators= [InputRequired(), Length(min = 6, max = 20)], 
                           render_kw= {"placeholder" : "UserName"})
    
    password = PasswordField(validators= [InputRequired(), Length(min= 8, max= 20)],
                             render_kw= {"placeholder" : "Password"})
    
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(validators= [InputRequired(), Length(min = 6, max = 20)], 
                           render_kw= {"placeholder" : "UserName"})
    
    password = PasswordField(validators= [InputRequired(), Length(min= 8, max= 20)],
                             render_kw= {"placeholder" : "Password"})
    
    submit = SubmitField("Register")
    '''
    def validate_username(self, username):
        existing_user_username = check_username(aiven_engine, username)
        if existing_user_username:
            raise ValidationError("The username already exists. Please choose a different one.")
    '''



class User(UserMixin):
    def __init__(self, id, username, password) -> None:
        self.id = id
        self.username = username 
        self.password = password
    
    @staticmethod
    def get_by_id(engine, user_id):
        with engine.connect() as conn:
            sql = "SELECT ID, User_name, Passkey FROM Users WHERE id = :ID"
            result = conn.execute(text(sql), {'ID': str(user_id)})
            result = result.all()[0]

            if result:
                # Assuming result is (id, username, password)
                return User(id=result[0], username=result[1], password=result[2])
            else:
                return None


@app.route("/")
def hello_world():
    Jobs = loadJobs(aiven_engine)
    return render_template("home.html", hURL = hosting_url, jobs = Jobs, abtUs = about_us)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    # After we submit the form...
    if form.validate_on_submit():
        new_user = {}
        hashed_password = b_crypt.generate_password_hash(form.password.data)
        new_user['username'] = form.username.data
        new_user['password'] = hashed_password
        add_user(aiven_engine, new_user)
        time.sleep(2)     # Redirects to login after 2 seconds. 
        return redirect(url_for('login'))

    return render_template('register.html', form = form)

@login_manager.user_loader
def load_user(user_id):
    # Use the user_id to fetch the user from the database
    return User.get_by_id(aiven_engine, user_id)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_username = return_existing_username(aiven_engine, form.username.data)
        if existing_username:
            id = existing_username[0]
            username = existing_username[1]
            password = existing_username[2]
            if b_crypt.check_password_hash(password, form.password.data):
                login_user(User(id, username, password))
                return redirect(url_for('test123'))
    return render_template('login.html', form = form)

@app.route("/test123", methods = ['POST', 'GET'])
@login_required
def test123():
    return "You are logged in..."

@app.route("/api/jobs")    # api-endpoint 1.0: Returns job details as json
def job_details():
    Jobs = loadJobs(aiven_engine)
    for i in range(len(Jobs)):
        Jobs[i] = dict(Jobs[i])
    return jsonify(Jobs)

@app.route("/job/<ID>")
def get_job_by_ID(ID):
    Job = loadJob(aiven_engine, ID)
    if Job:
        # Splitting the requirements and responsibilities...
        Job = dict(Job)
        if Job["Requirements"]:
            Job['Requirements'] = Job['Requirements'].split('.')
            Job["Requirements"].pop(-1)
        
        if Job['Responsibilities']:
            Job['Responsibilities'] = Job['Responsibilities'].split('.')
            Job["Responsibilities"].pop(-1)
        
        return render_template("Job_Page.html", job = Job)
    else:
        return f"No Job entry found under {ID} :(", 404

@app.route("/job/<ID>/apply", methods = ['GET','POST'])
def apply_job(ID):
    job = loadJob(aiven_engine, ID)
    if job:
        return render_template('applicationForm.html', job = job)
    else:
        return "Job post expired"

@app.route("/job/<ID>/review", methods = ['GET', 'POST'])
def application_submitted(ID):
    global data               # Because of this, this application is not meant for multiple access. 
    data = request.form
    data = dict(data)
    data['techStack'] = request.form.getlist('techStack')
    return render_template('reviewApplication.html', data = data, ID = ID)

@app.route("/job/<ID>/confirm", methods = ['POST'])
def confirm_submission(ID):
    global data
    add_application_to_DB(aiven_engine, ID, data)
    return render_template('applicationSuccess.html', ID = ID)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)
    # add_job()
