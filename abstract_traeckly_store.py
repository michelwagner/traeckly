from typing import Optional, List, Tuple


class AbstractTraecklyStore:
    """Interface for storage implementations that persist task tracking data."""

    def ensure_schema(self) -> None:
        """Ensure the storage schema exists."""
        raise NotImplementedError()

    def insert_task(self, task_name: str, starttime_isotime: str) -> None:
        """Insert a new task entry with the given start time."""
        raise NotImplementedError()

    def get_last_task(self) -> Optional[Tuple[int, str, Optional[float]]]:
        """Return the most recent task row as (id, starttime, duration)."""
        raise NotImplementedError()

    def update_duration(self, row_id: int, duration_seconds: float) -> None:
        """Update the duration of a task row."""
        raise NotImplementedError()

    def sum_total_duration(self, from_isotime: str, to_isotime: str) -> Optional[float]:
        """Return the total duration for tasks within a time range."""
        raise NotImplementedError()

    def sum_task_durations(self, from_isotime: str, to_isotime: str) -> List[Tuple[str, Optional[float]]]:
        """Return per-task duration totals within a time range."""
        raise NotImplementedError()

    def get_task_durations_sum(self, from_isotime: str, to_isotime: str) -> List[Tuple[str, Optional[float]]]:
        """Return individual task durations within a time range."""
        raise NotImplementedError()

    def commit(self) -> None:
        """Persist pending changes."""
        raise NotImplementedError()

    def close(self) -> None:
        """Close the storage backend."""
        raise NotImplementedError()
