import traeckly
import traeckly_gui
import unittest
from datetime import datetime, timedelta


class Test_Traeckli_argument_parsing(unittest.TestCase):
    def test_traeckly_argument_start(self):
        args = traeckly.parse_arguments(['start', 'Task-999'])
        self.assertEqual(args['command'], 'start')
        self.assertEqual(args['task_name'], 'Task-999')


    def test_traeckly_argument_stop(self):
        args = traeckly.parse_arguments(['stop'])
        self.assertEqual(args['command'], 'stop')


    def test_traeckly_argument_report(self):
        args = traeckly.parse_arguments(['report', '7d'])
        self.assertEqual(args['command'], 'report')
        self.assertEqual(args['timespan'], ['7d'])

        args = traeckly.parse_arguments(['report', 't1', 't2'])
        self.assertEqual(args['command'], 'report')
        self.assertEqual(args['timespan'], ['t1', 't2'])


    def test_traeckly_argument_timespan(self):
        from_to_time = traeckly.get_from_to_time_iso(['2023-04-09 11:45:21', '2023-04-16 23:59:59'])
        self.assertEqual(from_to_time[0], '2023-04-09T11:45:21')
        self.assertEqual(from_to_time[1], '2023-04-16T23:59:59')

        from_to_time = traeckly.get_from_to_time_iso(['2023-04-09', '2023-04-16'])
        self.assertEqual(from_to_time[0], '2023-04-09T00:00:00')
        self.assertEqual(from_to_time[1], '2023-04-16T00:00:00')

        from_to_time = traeckly.get_from_to_time_iso(['2023-04-09 11:45', '2023-04-16 23'])
        self.assertEqual(from_to_time[0], '2023-04-09T11:45:00')
        self.assertEqual(from_to_time[1], '2023-04-16T23:00:00')

        # Numeric day span should start at midnight and end at now
        now = datetime.now()
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        expected_start = start_of_today - timedelta(days=1)
        from_to_time = traeckly.get_from_to_time_iso(['2'])
        t1 = datetime.fromisoformat(from_to_time[0])
        t2 = datetime.fromisoformat(from_to_time[1])
        self.assertEqual(t1, expected_start)
        delta = abs((t2 - now).total_seconds())
        self.assertLess(delta, 5)


    def test_traeckly_argument_timespan_day(self):
        """Test that 'day' timespan starts from beginning of current day."""
        from_to_time = traeckly.get_from_to_time_iso(['day'])
        
        # Parse the returned ISO times
        t1 = datetime.fromisoformat(from_to_time[0])
        t2 = datetime.fromisoformat(from_to_time[1])
        
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
        from_to_time = traeckly.get_from_to_time_iso(['week'])
        
        # Parse the returned ISO times
        t1 = datetime.fromisoformat(from_to_time[0])
        t2 = datetime.fromisoformat(from_to_time[1])
        
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
        from_to_time = traeckly.get_from_to_time_iso(['month'])
        
        # Parse the returned ISO times
        t1 = datetime.fromisoformat(from_to_time[0])
        t2 = datetime.fromisoformat(from_to_time[1])
        
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
        from_to_time = traeckly.get_from_to_time_iso(['not-a-number'])
        self.assertEqual(from_to_time, ('', ''))

        from_to_time = traeckly.get_from_to_time_iso(['bad-date', 'also-bad'])
        self.assertEqual(from_to_time, ('', ''))


if __name__ == '__main__':
    unittest.main()
