import os
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DatabaseError

dbusername = "postgres" 
dbpass = "tnt" 
engine = create_engine('postgresql+psycopg2://{}:{}@172.17.0.3:5432'.format(dbusername, dbpass))
session = sessionmaker(bind=engine)()
session.connection().connection.set_isolation_level(0)
try:
    session.execute("CREATE DATABASE test_db") #create db
except DatabaseError as e:
    print("database already exists")
engine = create_engine('postgresql+psycopg2://{}:{}@172.17.0.3:5432/test_db'.format(dbusername, dbpass))
session = sessionmaker(bind=engine)()
session.connection().connection.set_isolation_level(1)
Base = declarative_base()

class TestRun(Base):
    __tablename__ = "test_run"

    id = Column("Id", Integer, primary_key=True)
    environment = Column(String(20))
    test = Column(String(20))
    created_at = Column(DateTime)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    status = Column(String(20))
    logs = Column(String)
    
    def __init__(self, environment=None, test=None, created_at=None, started_at=None, finished_at=None, status=None, logs=None):
        self.environment = environment
        self.test = test
        self.created_at = created_at
        self.started_at = started_at
        self.finished_at = finished_at
        self.status = status
        self.logs = logs

# create tables
Base.metadata.create_all(engine)
