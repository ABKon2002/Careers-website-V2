from sqlalchemy import create_engine, text
import os


class DataOperations:
    def __init__(self):
        '''Initializes an engine to the connected database.'''
        # Access environment variables (Aiven DB credentials)
        db_host = os.environ.get('DB_HOST')
        db_port = os.environ.get('DB_PORT')
        db_name = os.environ.get('DB_NAME')
        db_user = os.environ.get('DB_USER')
        db_password = os.environ.get('DB_PASSWORD')

        conn_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = None
        engine = create_engine(conn_string)
        if engine:
            # print("Successfully created an engine for the database...")
            self.engine = engine
        else:
            print("Database Connection failed!")
    
    def loadJobs(self, query = "select * from jobs"):
        ''' Returns the list of jobs in the DB. Can ask other queries using query = param as well.'''
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            resultAll = result.all()
            resDicts = []
            for row in resultAll:
                resDict = row._mapping
                resDicts.append(resDict)
            return resDicts
    
    def loadJob(self, ID):
        ''' Returns the entry of a job by its ID in the DB'''
        with self.engine.connect() as conn:
            result = conn.execute(text(f"Select * from jobs where ID = {ID}"))
            result = result.all()
            if len(result) == 0:
                return None
            else:
                return result[0]._mapping
    
    def add_application_to_DB(self, ID, application):
        """ Adds an input application dictionary into the applications table in the DB."""
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

        with self.engine.connect() as conn:
            conn.execute(text(query), params)
            conn.commit()
            return 1

    def check_username(self, username):
        """Checks is another user exists with the same username."""
        with self.engine.connect() as conn:
            query = f"Select * from Users where User_name = {username}"
            result = conn.execute(text(query))
            result = result.all()
            if len(result) == 0:
                return False
            return True

    def add_user(self, user):
        """Adds a registered user to the DB"""
        with self.engine.connect() as conn:
            query = f"Insert into Users(User_name, Passkey) values (:username, :password)"
            conn.execute(text(query), user)
            conn.commit()
            return 1
    
    def return_existing_username(self, username):
        """Return a username if it exists in the DB"""
        with self.engine.connect() as conn:
            query = f"Select * from Users where User_name = '{username}'"
            result = conn.execute(text(query))
            result = result.all()
            if len(result) == 0:
                return False
            return result[0]    # Returns a tuple of the user data.

    def applications_by_job(self):
        """Returns the available applications categorized by the Job IDs"""
        with self.engine.connect() as conn:
            query = '''select A.Application_ID as ID, J.ID as Job_ID, J.Title, 
                    A.first_name, A.Last_Name, A.Gender, A.Age, A.Nationality, 
                    A.Qualification from jobs as J join applications as A on 
                    J.ID = A.Job_ID order by Job_ID'''
            result = conn.execute(text(query))
            result = result.all()
            applications_by_job = {}
            for application in result:
                pass

