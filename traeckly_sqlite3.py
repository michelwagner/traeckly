from traeckly_service import TraecklyBackendInterface
from datetime import datetime
import time
import sqlite3

database = 'tracking.db'

class TraecklySQLiteBackend(TraecklyBackendInterface):
    sql_create_table = """CREATE TABLE IF NOT EXISTS "tracking" (
        "id" INTEGER,
        "task" TEXT,
        "starttime" INTEGER,
        "duration" INTEGER DEFAULT NULL,
        PRIMARY KEY("id"))"""
    sql_start_task = "INSERT INTO tracking VALUES (NULL, '{}', '{}', NULL)"
    sql_get_last_task = "SELECT id, starttime, duration FROM tracking ORDER BY id DESC LIMIT 1"
    sql_update_duration = "UPDATE tracking SET duration={} WHERE id={}"
    sql_sum_task_duration_from_to = "SELECT task, SUM(duration) FROM tracking WHERE starttime BETWEEN '{}' AND '{}' GROUP BY task"
    sql_sum_total_duration_from_to = "SELECT SUM(duration) FROM tracking WHERE starttime BETWEEN '{}' AND '{}'"


    def __init__(self):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.create_database()


    def __del__(self):
        self.conn.commit()
        self.conn.close()


    def create_database(self):
        self.database_execute(self.sql_create_table)
        

    def start_task(self, id):
        self.update_duration_of_last_task()
        
        if (id != None):
            self.database_execute(self.sql_start_task.format(id, self.get_isotimestring()))
            
        self.conn.commit()


    def update_duration_of_last_task(self):
        isotimestring_now = self.get_isotimestring()

        a = self.database_execute(self.sql_get_last_task)
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

                self.database_execute(self.sql_update_duration.format(duration, row_id))
        

    def get_task_durations(self, from_isotime, to_isotime):
        tasks = []

        result = self.database_execute(self.sql_sum_total_duration_from_to.format(from_isotime, to_isotime))
        entries = result.fetchall()
        total_duration = entries[0][0]
        task = (self.get_task_duration('Total', total_duration))
        if (task != None):
            tasks.append(task)

        result = self.database_execute(self.sql_sum_task_duration_from_to.format(from_isotime, to_isotime))
        entries = result.fetchall()

        for entry in entries:
            task_name = entry[0]
            task_duration_seconds = entry[1]
            task = (self.get_task_duration(task_name, task_duration_seconds))
            if (task != None):
                tasks.append(task)
            
        return tasks


    def get_task_duration(self, task_name, task_duration_seconds):
        if (task_duration_seconds != None):
            task_duration_string = self.format_time_difference(task_duration_seconds)
            task = (task_name, task_duration_string)
        else:
            task = None
           
        return task


    def get_isotimestring(self):
        return datetime.now().isoformat(timespec='seconds')


    def database_execute(self, statement):
        return self.cursor.execute(statement)


    def format_time_difference(self, delta_time_seconds):
        hours = delta_time_seconds // 3600
        minutes = round((delta_time_seconds - (hours * 3600.0)) / 60.0)
        return "{}:{:02d}".format(hours, minutes)
