from traeckly_service import TraecklyBackendBase
from abstract_traeckly_store import AbstractTraecklyStore
from datetime import datetime
from typing import Optional, Union, List, Tuple, Dict
import sqlite3


class TraecklySQLiteStore(AbstractTraecklyStore):
    """SQLite-backed store for task tracking data."""
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
    _sql_get_task_durations_from_to = "SELECT task, duration FROM tracking WHERE starttime BETWEEN ? AND ?"

    def __init__(self, database_path: str) -> None:
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self._closed = False
        self.ensure_schema()


    def __del__(self) -> None:
        if not self._closed:
            self.close()


    def ensure_schema(self) -> None:
        self._database_execute(self._sql_create_table)


    def insert_task(self, task_name: str, starttime_isotime: str) -> None:
        self._database_execute(self._sql_start_task, (task_name, starttime_isotime))


    def get_last_task(self) -> Optional[Tuple[int, str, Optional[float]]]:
        result = self._database_execute(self._sql_get_last_task)
        row = result.fetchone()
        return row if row is not None else None


    def update_duration(self, row_id: int, duration_seconds: float) -> None:
        self._database_execute(self._sql_update_duration, (duration_seconds, row_id))


    def sum_total_duration(self, from_isotime: str, to_isotime: str) -> Optional[float]:
        result = self._database_execute(self._sql_sum_total_duration_from_to, (from_isotime, to_isotime))
        entry = result.fetchone()
        if entry is None:
            total_duration = None
        else:
            total_duration = entry[0]            
        return total_duration


    def sum_task_durations(self, from_isotime: str, to_isotime: str) -> List[Tuple[str, Optional[float]]]:
        result = self._database_execute(self._sql_sum_task_duration_from_to, (from_isotime, to_isotime))
        return result.fetchall()


    def get_task_durations_sum(self, from_isotime: str, to_isotime: str) -> List[Tuple[str, Optional[float]]]:
        """Return individual task durations within a time range."""
        result = self._database_execute(self._sql_get_task_durations_from_to, (from_isotime, to_isotime))
        return result.fetchall()


    def commit(self) -> None:
        self.conn.commit()


    def close(self) -> None:
        self.conn.commit()
        self.conn.close()
        self._closed = True


    def _database_execute(self, statement: str, params: Optional[Tuple[object, ...]] = None) -> sqlite3.Cursor:
        if params is None:
            result = self.cursor.execute(statement)
        else:
            result = self.cursor.execute(statement, params)
        return result


class TraecklyBackend(TraecklyBackendBase):
    """Store-agnostic backend for task tracking data."""

    def __init__(self, store: AbstractTraecklyStore) -> None:
        self.store = store


    def close(self) -> None:
        self.store.close()


    def start_task(self, task_name: Optional[str]) -> None:
        """Start tracking a task or stop tracking if task_name is None."""
        self._update_duration_of_last_task()

        if task_name is not None:
            task_name = self._normalize_task_name(task_name)
            self.store.insert_task(task_name, self._get_isotimestring())

        self.store.commit()


    def _update_duration_of_last_task(self) -> None:
        """Update the duration of the most recent task if it is still open."""
        last_task = self.store.get_last_task()
        if last_task is not None:
            duration = last_task[2]

            if duration is None:
                row_id = last_task[0]
                isotimestring_start = last_task[1]
                isotimestring_now = self._get_isotimestring()

                t1 = datetime.fromisoformat(isotimestring_start)
                t2 = datetime.fromisoformat(isotimestring_now)
                delta = t2 - t1
                duration = delta.total_seconds()

                self.store.update_duration(row_id, duration)


    def get_task_durations_sum(self, from_isotime: str, to_isotime: str) -> Dict[str, Union[str, List[Tuple[str, str]]]]:
        """Return total and per-task durations for a time range."""
        tasks = []

        total_duration = self.store.sum_total_duration(from_isotime, to_isotime)
        total_task = self._get_task_duration('Total', total_duration)
        if total_task is not None:
            tasks.append(total_task)

        entries = self.store.sum_task_durations(from_isotime, to_isotime)

        for entry in entries:
            task_name = entry[0]
            task_duration_seconds = entry[1]
            task = self._get_task_duration(task_name, task_duration_seconds)
            if task is not None:
                tasks.append(task)

        return {"from": from_isotime, "to": to_isotime, "tasks": tasks}


    def _get_task_duration(self, task_name: str, task_duration_seconds: Optional[float]) -> Optional[Tuple[str, str]]:
        """Format a single task duration into a display tuple."""
        if task_duration_seconds is not None:
            task_duration_string = self._format_time_difference(task_duration_seconds)
            task = (task_name, task_duration_string)
        else:
            task = None
        return task


    def _get_isotimestring(self) -> str:
        """Return the current time as an ISO-8601 string."""
        return datetime.now().isoformat(timespec='seconds')
