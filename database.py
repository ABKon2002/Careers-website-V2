
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
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

database_url = os.environ.get('DATABASE_URL')

# Access environment variables (Aiven DB credentials)
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

aiven_engine = connectDBcred(db_host, db_port, db_user, db_password, db_name)
jobs = loadJobs(aiven_engine)
