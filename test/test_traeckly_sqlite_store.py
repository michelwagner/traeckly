import unittest

from traeckly_sqlite3 import TraecklySQLiteStore


class TestTraecklySQLiteStore(unittest.TestCase):
    def setUp(self) -> None:
        self.store = TraecklySQLiteStore(":memory:")

    def tearDown(self) -> None:
        self.store.close()

    def test_empty_last_task(self) -> None:
        self.assertIsNone(self.store.get_last_task())

    def test_insert_update_and_sum(self) -> None:
        self.store.insert_task("Task_A", "2026-01-01T00:00:00")
        last_task = self.store.get_last_task()
        self.assertIsNotNone(last_task)
        self.store.update_duration(last_task[0], 3600.0)

        self.store.insert_task("Task_B", "2026-01-01T01:00:00")
        last_task = self.store.get_last_task()
        self.assertIsNotNone(last_task)
        self.store.update_duration(last_task[0], 1800.0)

        total = self.store.sum_total_duration("2026-01-01T00:00:00", "2026-01-01T02:00:00")
        self.assertEqual(total, 5400.0)

        per_task = dict(self.store.sum_task_durations("2026-01-01T00:00:00", "2026-01-01T02:00:00"))
        self.assertEqual(per_task["Task_A"], 3600.0)
        self.assertEqual(per_task["Task_B"], 1800.0)

    def test_get_task_durations_sum_returns_individual_entries(self) -> None:
        self.store.insert_task("Task_A", "2026-01-01T00:00:00")
        last_task = self.store.get_last_task()
        self.assertIsNotNone(last_task)
        self.store.update_duration(last_task[0], 3600.0)

        self.store.insert_task("Task_B", "2026-01-01T01:00:00")
        last_task = self.store.get_last_task()
        self.assertIsNotNone(last_task)
        self.store.update_duration(last_task[0], 1800.0)

        self.store.insert_task("Task_A", "2026-01-01T01:30:00")
        last_task = self.store.get_last_task()
        self.assertIsNotNone(last_task)
        self.store.update_duration(last_task[0], 900.0)

        self.store.insert_task("Task_C", "2026-01-01T03:00:00")
        last_task = self.store.get_last_task()
        self.assertIsNotNone(last_task)
        self.store.update_duration(last_task[0], 600.0)

        durations = self.store.get_task_durations_sum("2026-01-01T00:00:00", "2026-01-01T02:00:00")

        self.assertCountEqual(
            durations,
            [
                ("Task_A", 3600.0),
                ("Task_B", 1800.0),
                ("Task_A", 900.0),
            ],
        )


if __name__ == "__main__":
    unittest.main()
