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

from os.path import dirname, abspath, join, exists
from functions import get_config

current_dir = dirname(dirname(abspath(__file__)))

#from functions import get_config

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

def setup_db():
    config_path = current_dir+"/config.yaml"
    db_username = get_config("POSTGRES_DB_DETAILS", "USERNAME", config_path)
    db_password = get_config("POSTGRES_DB_DETAILS", "PASSWORD", config_path)
    db_ip_port = get_config("POSTGRES_DB_DETAILS", "SERVER_IP", config_path)+ ":"\
                       + get_config("POSTGRES_DB_DETAILS", "PORT", config_path)
    engine = create_engine('postgresql+psycopg2://{}:{}@{}'.format(db_username, db_password, db_ip_port))
    session = sessionmaker(bind=engine)()
    session.connection().connection.set_isolation_level(0)
    try:
        session.execute("CREATE DATABASE test_db") #create db
    except DatabaseError as e:
        print("database already exists")
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/test_db'.format(db_username, db_password, db_ip_port))
    session = sessionmaker(bind=engine)()
    session.connection().connection.set_isolation_level(1)

    # create tables
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    setup_db()
