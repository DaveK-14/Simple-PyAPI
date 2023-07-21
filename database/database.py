from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
def db_connect(user, password, location, port, dbName):
    print(f"mysql+mysqlconnector://{user}:{password}@{location}:{port}/{dbName}")
    return create_engine(f"mysql+mysqlconnector://{user}:{password}@{location}:{port}/{dbName}", echo = True)