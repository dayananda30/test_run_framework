import os
import time
from os.path import dirname, abspath

from postgre_models.models import TestRun
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from functions import get_config

current_dir = dirname(dirname(abspath(__file__)))


class DBSession:
    def __init__(self):
        print(current_dir)
        config_path = current_dir+"/config.yaml"
        self.db_username = get_config("POSTGRES_DB_DETAILS", "USERNAME", config_path)
        self.db_password = get_config("POSTGRES_DB_DETAILS", "PASSWORD", config_path) 
        self.db_ip_port = get_config("POSTGRES_DB_DETAILS", "SERVER_IP", config_path)+ ":"\
                           + get_config("POSTGRES_DB_DETAILS", "PORT", config_path)
        self.engine = create_engine('postgresql+psycopg2://{}:{}@{}/test_db'.format(self.db_username, self.db_password, self.db_ip_port))
        self.session = sessionmaker(bind=self.engine)()
        self.session.connection().connection.set_isolation_level(1)

    def create_entry(self):
        """
        This part is from Vm to container.
        """
        testcase = TestRun(created_at=datetime.utcnow(), status="Queued")
        self.session.add(testcase)
        self.session.commit()
        return testcase.id

    def update_new_query(self, test_id, update_data):
        start_date = datetime.utcnow()
        end_date = datetime.utcnow()
        self.session.query(TestRun).filter(TestRun.id == test_id).update(update_data)
        self.session.commit()

    def update_query(self, id):
        date1 = datetime.utcnow()
        query = sqlalchemy.update(TestRun).values(started_at = date1)
        query = query.where(TestRun.id == id)
        self.session.execute(query)
        self.session.commit()

    def get_all_records(self):
        list_obj = []
        for obj in self.session.query(TestRun).all():
            list_obj.append(obj.__dict__)
        return list_obj

    def get_one_record(self, test_id):
        try:
            result = self.session.query(TestRun).filter(TestRun.id==test_id).one()
            return result.__dict__
        except NoResultFound:
            return "Test case with id - {} not found.".format(test_id)

    def session_close(self):
        self.session.close()
    
if __name__ == "__main__":
    db = DBSession()
    db.create_entry()
    #db.update_new_query(3)
    db.session_close()
