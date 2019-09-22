import os
from models import TestRun
from datetime import datetime
import sqlalchemy
import time

class DBSession:
    def __init__(self):
        self.dbusername = "postgres" 
        self.dbpass = "tnt" 
        self.engine = sqlalchemy.create_engine('postgresql+psycopg2://{}:{}@172.17.0.3:5432/test_db'.format(self.dbusername, self.dbpass))
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
        self.session.connection().connection.set_isolation_level(1)

    def create_entry(self):
        """
        This part is from Vm to container.
        """
        testcase = TestRun(created_at=datetime.utcnow(), status="Queued")
        self.session.add(testcase)
        self.session.commit()
        print(testcase.id)

    def update_new_query(self, test_id, update_data):
        start_date = datetime.utcnow()
        #time.sleep(61)
        end_date = datetime.utcnow()
#        update_data = {'started_at': start_date, 'finished_at': end_date, 'environment': 'test_env_1'}
        self.session.query(TestRun).filter(TestRun.id == test_id).update(update_data)
        #self.session.query(TestRun).filter(TestRun.id == test_id).update({'started_at': start_date})
        self.session.commit()

    def update_query(self, id):
        date1 = datetime.utcnow()
        query = sqlalchemy.update(TestRun).values(started_at = date1)
        query = query.where(TestRun.id == id)
        self.session.execute(query)
        self.session.commit()

    def get_all_records(self):
        query = sqlalchemy.select([TestRun])
        return self.session.execute(query).fetchall()

    def get_one_record(self, id):
        query = sqlalchemy.select([TestRun]).where(TestRun.id==id)
        ResultProxy = self.session.execute(query)
        return ResultProxy.fetchall()

    def session_close(self):
        self.session.close()
    
if __name__ == "__main__":
    db = DBSession()
    #db.create_entry()
    #db.update_new_query(3)
    db_output = db.get_one_record(3)
    logs = db_output[-1][-1]
    print(logs)
    
    db.session_close()
