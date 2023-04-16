import traeckly
import unittest

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
        from_to_time = traeckly.get_from_to_isotimes(['2023-04-09 11:45:21', '2023-04-16 23:59:59'])
        self.assertEqual(from_to_time[0], '2023-04-09T11:45:21')
        self.assertEqual(from_to_time[1], '2023-04-16T23:59:59')

        from_to_time = traeckly.get_from_to_isotimes(['2023-04-09', '2023-04-16'])
        self.assertEqual(from_to_time[0], '2023-04-09T00:00:00')
        self.assertEqual(from_to_time[1], '2023-04-16T00:00:00')

        from_to_time = traeckly.get_from_to_isotimes(['2023-04-09 11:45', '2023-04-16 23'])
        self.assertEqual(from_to_time[0], '2023-04-09T11:45:00')
        self.assertEqual(from_to_time[1], '2023-04-16T23:00:00')


if __name__ == '__main__':
    unittest.main()
