from traeckly_service import TraecklyBackendBase
from datetime import datetime
from typing import Optional
import sqlite3


class TraecklySQLiteBackend(TraecklyBackendBase):
    """SQLite-backed storage for task tracking data."""
    _sql_create_table = """CREATE TABLE IF NOT EXISTS "tracking" (
        "id" INTEGER,
        "task" TEXT,
        "starttime" INTEGER,
        "duration" INTEGER DEFAULT NULL,
        PRIMARY KEY("id"))"""
    _sql_start_task = "INSERT INTO tracking VALUES (NULL, ?, ?, NULL)"
    _sql_get_last_task = "SELECT id, starttime, duration FROM tracking ORDER BY id DESC LIMIT 1"
    _sql_update_duration = "UPDATE tracking SET duration=? WHERE id=?"
    _sql_sum_task_duration_from_to = "SELECT task, SUM(duration) FROM tracking WHERE starttime BETWEEN ? AND ? GROUP BY task"
    _sql_sum_total_duration_from_to = "SELECT SUM(duration) FROM tracking WHERE starttime BETWEEN ? AND ?"
    _closed = False


    def __init__(self, database_path: str) -> None:
        """Initialize the backend with a SQLite database path."""
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self._create_database()


    def __del__(self) -> None:
        """Ensure the database connection is closed when the object is deleted."""
        if not self._closed:
            self.close()


    def close(self) -> None:
        """Commit and close the database connection."""
        self.conn.commit()
        self.conn.close()
        self._closed = True


    def _create_database(self) -> None:
        """Ensure the tracking table exists."""
        self._database_execute(self._sql_create_table)
        

    def start_task(self, task_name: Optional[str]) -> None:
        """Start tracking a task or stop tracking if task_name is None."""
        self._update_duration_of_last_task()
        
        if (task_name != None):
            task_name = self._normalize_task_name(task_name)
            self._database_execute(self._sql_start_task, (task_name, self._get_isotimestring()))
            
        self.conn.commit()


    def _update_duration_of_last_task(self) -> None:
        """Update the duration of the most recent task if it is still open."""
        isotimestring_now = self._get_isotimestring()

        a = self._database_execute(self._sql_get_last_task)
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

                self._database_execute(self._sql_update_duration, (duration, row_id))
        

    def get_task_durations(self, from_isotime: str, to_isotime: str) -> dict[str, str | list[tuple[str, str]]]:
        """Return total and per-task durations for a time range."""
        tasks = []

        result = self._database_execute(self._sql_sum_total_duration_from_to, (from_isotime, to_isotime))
        entries = result.fetchall()
        total_duration = entries[0][0]
        task = (self._get_task_duration('Total', total_duration))
        if (task != None):
            tasks.append(task)

        result = self._database_execute(self._sql_sum_task_duration_from_to, (from_isotime, to_isotime))
        entries = result.fetchall()

        for entry in entries:
            task_name = entry[0]
            task_duration_seconds = entry[1]
            task = (self._get_task_duration(task_name, task_duration_seconds))
            if (task != None):
                tasks.append(task)
            
        return {"from": from_isotime, "to": to_isotime, "tasks": tasks}


    def _get_task_duration(self, task_name: str, task_duration_seconds: Optional[float]) -> Optional[tuple[str, str]]:
        """Format a single task duration into a display tuple."""
        if (task_duration_seconds != None):
            task_duration_string = self._format_time_difference(task_duration_seconds)
            task = (task_name, task_duration_string)
        else:
            task = None
           
        return task


    def _get_isotimestring(self) -> str:
        """Return the current time as an ISO-8601 string."""
        return datetime.now().isoformat(timespec='seconds')


    def _database_execute(self, statement: str, params: Optional[tuple[object, ...]] = None) -> sqlite3.Cursor:
        """Execute a SQL statement and return the cursor."""
        if (params is None):
            result = self.cursor.execute(statement)
        else:
            result = self.cursor.execute(statement, params)
            
        return result