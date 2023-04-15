import sys
from traeckly_service import TraecklyBackendInterface, TraecklyService
from datetime import datetime
import time
import sqlite3

# SELECT id,starttime FROM tracking ORDER BY id DESC LIMIT 1
# UPDATE tracking SET duration=77 WHERE ROWID=7
# INSERT INTO tracking VALUES (NULL, 'Task-Name', 1, '07:45:00', 0)
# SELECT id, task, starttime, SUM(duration) FROM tracking WHERE starttime BETWEEN '2022-04-13 00:00:00' AND '2024-04-13 23:59:59' GROUP BY task

class TraecklySQLiteBackend(TraecklyBackendInterface):
    def __init__(self):
        self.conn = sqlite3.connect('tracking.sql')
        self.cursor = self.conn.cursor()


    def __del__(self):
        self.conn.commit()
        self.conn.close()


    def create_database(self):
        self.database_execute("""
                    CREATE TABLE "tracking" (
                	"id" INTEGER,
                	"task" TEXT,
                	"starttime" INTEGER,
                	"duration" INTEGER DEFAULT NULL,
                	PRIMARY KEY("id"))
            """)
        

    def start_task(self, id):
        self.update_duration_of_last_task()
        self.database_execute("INSERT INTO tracking VALUES (NULL, '{}', '{}', NULL)".format(id, self.get_isotimestring()))
        self.conn.commit()


    def update_duration_of_last_task(self):
        isotimestring_now = self.get_isotimestring()

        a = self.database_execute("SELECT id, starttime, duration FROM tracking ORDER BY id DESC LIMIT 1")
        d = a.fetchone()
        if (d != None):
            duration = d[2]
            
            if (duration == None):
                row_id = d[0]
                isotimestring_start = d[1]

                t1 = datetime.fromisoformat(isotimestring_start)
                t2 = datetime.fromisoformat(isotimestring_now)
                d = t2-t1
                duration = d.total_seconds()

                self.database_execute("UPDATE tracking SET duration={} WHERE id={}".format(duration, row_id))
        

    def get_isotimestring(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')


    def database_execute(self, statement):
        return self.cursor.execute(statement)

        
if __name__ == "__main__":
    print('sqlite3 backend')

    backend = TraecklySQLiteBackend()
    service = TraecklyService(backend)
    
    service.start_task('Task-123')
    time.sleep(5)
    service.start_task('Break')
    time.sleep(2)
    service.start_task('Task-123')
