import unittest
from typing import Optional

from traeckly_sqlite3 import TraecklyBackend
from abstract_traeckly_store import AbstractTraecklyStore


class FakeStore(AbstractTraecklyStore):
    def __init__(self) -> None:
        self.entries: list[dict[str, object]] = []
        self.next_id = 1
        self.closed = False

    def ensure_schema(self) -> None:
        pass

    def insert_task(self, task_name: str, starttime_isotime: str) -> None:
        self.entries.append({
            "id": self.next_id,
            "task": task_name,
            "starttime": starttime_isotime,
            "duration": None
        })
        self.next_id += 1

    def get_last_task(self) -> Optional[tuple[int, str, Optional[float]]]:
        if not self.entries:
            return None
        entry = self.entries[-1]
        return (entry["id"], entry["starttime"], entry["duration"])  # type: ignore[return-value]

    def update_duration(self, row_id: int, duration_seconds: float) -> None:
        for entry in self.entries:
            if entry["id"] == row_id:
                entry["duration"] = duration_seconds
                return

    def sum_total_duration(self, from_isotime: str, to_isotime: str) -> Optional[float]:
        durations = [
            entry["duration"] for entry in self.entries
            if entry["duration"] is not None
            and from_isotime <= entry["starttime"] <= to_isotime
        ]
        return sum(durations) if durations else None

    def sum_task_durations(self, from_isotime: str, to_isotime: str) -> list[tuple[str, Optional[float]]]:
        totals: dict[str, float] = {}
        for entry in self.entries:
            if entry["duration"] is None:
                continue
            if not (from_isotime <= entry["starttime"] <= to_isotime):
                continue
            task_name = entry["task"]
            totals[task_name] = totals.get(task_name, 0.0) + float(entry["duration"])
        return [(task, duration) for task, duration in totals.items()]

    def commit(self) -> None:
        pass

    def close(self) -> None:
        self.closed = True


class FixedTimeBackend(TraecklyBackend):
    def __init__(self, store: AbstractTraecklyStore, times: list[str]) -> None:
        super().__init__(store)
        self._times = iter(times)

    def _get_isotimestring(self) -> str:
        return next(self._times)


class TestTraecklyTrackingBackend(unittest.TestCase):
    def test_start_and_stop_updates_duration(self) -> None:
        store = FakeStore()
        backend = FixedTimeBackend(
            store,
            ["2026-01-01T00:00:00", "2026-01-01T01:00:00"]
        )

        backend.start_task("Task A")
        backend.start_task(None)

        self.assertEqual(len(store.entries), 1)
        self.assertEqual(store.entries[0]["duration"], 3600.0)

    def test_get_task_durations_formats_output(self) -> None:
        store = FakeStore()
        backend = FixedTimeBackend(store, ["2026-01-01T00:00:00", "2026-01-01T01:00:00"])

        backend.start_task("Task A")
        backend.start_task(None)

        result = backend.get_task_durations("2026-01-01T00:00:00", "2026-01-01T02:00:00")

        self.assertEqual(result["from"], "2026-01-01T00:00:00")
        self.assertEqual(result["to"], "2026-01-01T02:00:00")
        self.assertIn(("Total", "1:00"), result["tasks"])
        self.assertIn(("Task_A", "1:00"), result["tasks"])


if __name__ == "__main__":
    unittest.main()
