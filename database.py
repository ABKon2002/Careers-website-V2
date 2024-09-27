
from sqlalchemy import create_engine, text
import os


def connectDBcred(host, port, user, password, dbName):
    '''Connect to a DB with the credentials.'''
    conn_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbName}'
    engine = None
    engine = create_engine(conn_string)
    if engine:
        # print("Successfully created an engine for the database...")
        return engine
    else:
        print("Database Connection failed!")

def loadJobs(engine, query = "select * from jobs"):
    ''' Returns the list of jobs in the DB'''
    with engine.connect() as conn:
        result = conn.execute(text(query))
        resultAll = result.all()
        resDicts = []
        for row in resultAll:
            resDict = row._mapping
            resDicts.append(resDict)
        return resDicts

def loadJob(engine, ID):
    ''' Returns the entry of a job by its ID in the DB'''
    with engine.connect() as conn:
        result = conn.execute(text(f"Select * from jobs where ID = {ID}"))
        result = result.all()
        if len(result) == 0:
            return None
        else:
            return result[0]._mapping

def add_application_to_DB(engine, ID, application):
    """ Adds an input application dictionary into the applications table in the DB """

    first_name = application['firstName']
    middle_name = application['middleName']
    last_name = application['lastName']
    gender = application['gender']
    age = int(application['age'])
    nationality = application['nationality']
    qualification = application['qualification']
    tech_stack = ', '.join(application['techStack'])
    current_title = application['currentJob']
    current_employer = application['currentEmployer']
    current_salary = int(application['currentSalary'])

    query = "INSERT INTO applications(Job_ID, First_name, Middle_name, Last_name, Gender, Age, Nationality, Qualification, Tech_stack, Current_title, Current_Employer, Current_salary) VALUES (:job_id, :first_name, :middle_name, :last_name, :gender, :age, :nationality, :qualification, :techStack, :current_title, :current_employer, :current_salary)"
    
    params = {
    "job_id": ID,
    "first_name": first_name,
    "middle_name": middle_name,
    "last_name": last_name,
    "gender": gender,
    "age": age,
    "nationality": nationality,
    "qualification": qualification,
    "techStack": tech_stack,
    "current_title": current_title,
    "current_employer": current_employer,
    "current_salary": current_salary
    }

    with engine.connect() as conn:
        conn.execute(text(query), params)
        conn.commit()


database_url = os.environ.get('DATABASE_URL')

# Access environment variables (Aiven DB credentials)
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

aiven_engine = connectDBcred(db_host, db_port, db_user, db_password, db_name)
