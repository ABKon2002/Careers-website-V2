
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


load_dotenv()

# Access environment variables (Aiven DB credentials)
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

aiven_engine = connectDBcred(db_host, db_port, db_user, db_password, db_name)
jobs = loadJobs(aiven_engine)
