
from flask import Flask, render_template, jsonify

app = Flask(__name__)

Jobs = [
    {
        "ID" : 1, 
        "Role" : "Frontend Engineer", 
        "Location" : "Bangalore, IND", 
        "Salary" : "Rs. 10 LPA"
    }, 
    {
        "ID" : 2, 
        "Role" : "Web Developer", 
        "Location" : "Bangalore, IND", 
        "Salary" : "Rs. 8 LPA"
    }, 
    {
        "ID" : 3, 
        "Role" : "Backend Developer", 
        "Location" : "Hyderabad, IND", 
        "Salary" : "Rs. 11 LPA"
    }, 
    {
        "ID" : 2, 
        "Role" : "Data Analyst", 
        "Location" : "Remote", 
        "Salary" : "Rs. 9 LPA"
    }
]

about_us = [
    "We believe in what people make possible.", 
    "Our mission is to empower every person and every organization on the planet to achieve more.", 
    "We believe technology can and should be a force for good and that meaningful innovation can and will contribute to a brighter world in big and small ways.", 
    "We believe that, when designed with people at the center, AI can extend your capabilities.",
    "As the world continues to respond to COVID-19, we are working to do our part by ensuring the safety of our employees."
]

@app.route("/")
def hello_world():
    return render_template("home.html", jobs = Jobs, abtUs = about_us)

@app.route("/api/jobs")    # api-endpoint 1.0: Returns job details as json
def job_details():
    return jsonify(Jobs)

def add_job():
    id = int(input("Enter Job ID: "))
    role = input("Enter Role: ")
    loc = input("Enter Location: ")
    salary = input("Enter Salary: ")
    Jobs.append({
        "ID" : id, 
        "Role" : role, 
        "Location" : loc, 
        "Salary" : salary
    })

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)
    # add_job()
