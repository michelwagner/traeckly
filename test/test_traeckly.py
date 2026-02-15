import traeckly
import traeckly_gui
import unittest
from datetime import datetime, timedelta


class Test_Traeckli_argument_parsing(unittest.TestCase):
    def test_traeckly_argument_start(self):
        """Parse 'start' command and task name."""
        args = traeckly.parse_arguments(['start', 'Task-999'])
        self.assertEqual(args['command'], 'start')
        self.assertEqual(args['task_name'], 'Task-999')


    def test_traeckly_argument_stop(self):
        """Parse 'stop' command without extra args."""
        args = traeckly.parse_arguments(['stop'])
        self.assertEqual(args['command'], 'stop')


    def test_traeckly_argument_report(self):
        """Parse 'report' command with one or two args."""
        args = traeckly.parse_arguments(['report', '7'])
        self.assertEqual(args['command'], 'report')
        self.assertEqual(args['timespan'], ['7'])

        args = traeckly.parse_arguments(['report', 't1', 't2'])
        self.assertEqual(args['command'], 'report')
        self.assertEqual(args['timespan'], ['t1', 't2'])


    def test_traeckly_argument_timespan_with_seconds(self):
        """Parse ISO times with seconds in both endpoints."""
        (from_time, to_time) = traeckly.get_from_to_time_iso(['2023-04-09 11:45:21', '2023-04-16 23:59:59'])
        self.assertEqual(from_time, '2023-04-09T11:45:21')
        self.assertEqual(to_time, '2023-04-16T23:59:59')


    def test_traeckly_argument_timespan_date_only(self):
        """Parse date-only inputs into midnight ISO times."""
        (from_time, to_time) = traeckly.get_from_to_time_iso(['2023-04-09', '2023-04-16'])
        self.assertEqual(from_time, '2023-04-09T00:00:00')
        self.assertEqual(to_time, '2023-04-16T00:00:00')


    def test_traeckly_argument_timespan_partial_time(self):
        """Parse partial time inputs with missing seconds or minutes."""
        (from_time, to_time) = traeckly.get_from_to_time_iso(['2023-04-09 11:45', '2023-04-16 23'])
        self.assertEqual(from_time, '2023-04-09T11:45:00')
        self.assertEqual(to_time, '2023-04-16T23:00:00')


    def test_traeckly_argument_timespan_numeric_days(self):
        """Numeric day spans start at midnight and end at now."""
        now = datetime.now()
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        expected_start = start_of_today - timedelta(days=1)
        (from_time, to_time) = traeckly.get_from_to_time_iso(['2'])
        t1 = datetime.fromisoformat(from_time)
        t2 = datetime.fromisoformat(to_time)
        self.assertEqual(t1, expected_start)
        delta = abs((t2 - now).total_seconds())
        self.assertLess(delta, 5)


    def test_traeckly_argument_timespan_day(self):
        """Test that 'day' timespan starts from beginning of current day."""
        (from_time, to_time) = traeckly.get_from_to_time_iso(['day'])
        
        # parse the returned ISO times
        t1 = datetime.fromisoformat(from_time)
        t2 = datetime.fromisoformat(to_time)
        
        now = datetime.now()

        # t1 should be today at 00:00:00
        self.assertEqual(t1.year, now.year)
        self.assertEqual(t1.month, now.month)
        self.assertEqual(t1.day, now.day)
        self.assertEqual(t1.hour, 0)
        self.assertEqual(t1.minute, 0)
        self.assertEqual(t1.second, 0)
        
        # t2 should be close to now (within a few seconds)
        delta = abs((t2 - now).total_seconds())
        self.assertLess(delta, 5)


    def test_traeckly_argument_timespan_week(self):
        """Test that 'week' timespan starts from beginning of current week (Monday)."""
        (from_time, to_time) = traeckly.get_from_to_time_iso(['week'])
        
        # parse the returned ISO times
        t1 = datetime.fromisoformat(from_time)
        t2 = datetime.fromisoformat(to_time)
        
        # t1 should be on a Monday at 00:00:00
        self.assertEqual(t1.weekday(), 0)  # 0 = Monday
        self.assertEqual(t1.hour, 0)
        self.assertEqual(t1.minute, 0)
        self.assertEqual(t1.second, 0)
        
        # t2 should be close to now (within a few seconds)
        now = datetime.now()
        delta = abs((t2 - now).total_seconds())
        self.assertLess(delta, 5)


    def test_traeckly_argument_timespan_month(self):
        """Test that 'month' timespan starts from beginning of current month."""
        (from_time, to_time) = traeckly.get_from_to_time_iso(['month'])
        
        # parse the returned ISO times
        t1 = datetime.fromisoformat(from_time)
        t2 = datetime.fromisoformat(to_time)
        
        # t1 should be on the 1st day of the month at 00:00:00
        self.assertEqual(t1.day, 1)
        self.assertEqual(t1.hour, 0)
        self.assertEqual(t1.minute, 0)
        self.assertEqual(t1.second, 0)
        
        # t2 should be close to now (within a few seconds)
        now = datetime.now()
        delta = abs((t2 - now).total_seconds())
        self.assertLess(delta, 5)
        
        # t1 and t2 should be in the same month
        self.assertEqual(t1.month, t2.month)
        self.assertEqual(t1.year, t2.year)


    def test_traeckly_argument_timespan_invalid_returns_empty(self):
        """Invalid timespan inputs should return empty strings."""
        (from_time, to_time) = traeckly.get_from_to_time_iso(['not-a-number'])
        self.assertEqual((from_time, to_time), ('', ''))

        (from_time, to_time) = traeckly.get_from_to_time_iso(['bad-date', 'also-bad'])
        self.assertEqual((from_time, to_time), ('', ''))


if __name__ == '__main__':
    unittest.main()
