
from flask import Flask, render_template, jsonify, request
from database import aiven_engine, loadJobs, loadJob, add_application_to_DB
import requests

app = Flask(__name__, template_folder="Templates")

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

@app.route("/")
def hello_world():
    Jobs = loadJobs(aiven_engine)
    return render_template("home.html", hURL = hosting_url, jobs = Jobs, abtUs = about_us)

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
    data = request.form
    data = dict(data)
    data['techStack'] = request.form.getlist('techStack')
    add_application_to_DB(aiven_engine, ID, data)
    return render_template('reviewApplication.html', data = data, ID = ID)

@app.route("/job/<ID>/confirm", methods = ['POST'])
def confirm_submission(ID):
    return render_template('applicationSuccess.html', ID = ID)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)
    # add_job()
