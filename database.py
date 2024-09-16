
from sqlalchemy import create_engine, text

engine = None
engine = create_engine("mysql+pymysql://avnadmin:AVNS_Uz0F7lT85disV7DWXX3@mysql-12483d59-careers-data.c.aivencloud.com/defaultdb?charset=utf8mb4")
if engine:
    print("Success")
    print(engine)
else:
    print("Connection failed!")

with engine.connect() as conn:
    result = conn.execute(text("Select * from jobs"))
    print(result.all())
