import sys
print(sys.path)
#sys.path.insert(0, '/home/wagm/projects/traeckly')
#import traeckly_service
from traeckly_service import TraecklyBackendInterface, TraecklyService

import time
import sqlite3


class TraecklySQLiteBackend(TraecklyBackendInterface):
    def __init__(self):
        self._start_time = 0
        self._active_task = None
        self.conn = sqlite3.connect('tracking.sql')
        self.c = self.conn.cursor()


    def __del__(self):
        self.conn.commit()
        self.conn.close()


    def create_database(self):
        self.c.execute("""
                CREATE TABLE "tracking" (
                "topic"	    TEXT NOT NULL,
                "action"	INTEGER NOT NULL,
                "timestamp"	TEXT NOT NULL,
                "duration"	INTEGER DEFAULT 0)
            """)
        

    def start_task(self, id):
        # if (self._active_task != None):
        #     self._show_delta_time()

        # self._start_time = time.time()
        self._active_task = id
        # self._log("{} started".format(id))
        self.c.execute("INSERT INTO tracking VALUES ('{}', 1, '07:45:00', 0)".format(id))


    # def _format_time_difference(self, delta_time):
    #     hours = int(delta_time) // 3600
    #     minutes = round((delta_time - (hours * 3600.0)) / 60.0)
    #     return "{}:{:02d}".format(hours, minutes)


    # def _log(self, message):
    #     logging.info(message)


if __name__ == "__main__":
    print('sqlite3 backend')

    backend = TraecklySQLiteBackend()
    service = TraecklyService(backend)
    service.start_task('Task-123')
    service.start_task('Break')
    service.start_task('Task-123')

# # create a connection
#     conn = sqlite3.connect('tracking.sql')

# # create a table
#     c = conn.cursor()  # cursor
# #    create_database(c)
#     c.execute("INSERT INTO tracking VALUES ('Task-123', 1, '06:45:12', 0)")

# # commit and close
#     conn.commit()
#     conn.close()    