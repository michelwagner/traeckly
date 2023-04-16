import traeckly
import unittest

class Test_Traeckli_cli(unittest.TestCase):
    def test_traeckly_cli_argument_parsing(self):
        args = traeckly.parse_arguments(['report'])
        self.assertEqual(args['weekly'], False)
        args = traeckly.parse_arguments(['report', '-w'])
        self.assertEqual(args['weekly'], True)
        args = traeckly.parse_arguments(['report', '--weekly'])
        self.assertEqual(args['weekly'], True)

        args = traeckly.parse_arguments(['start', 'Task-999'])
        self.assertEqual(args['start_task'], 'Task-999')


if __name__ == '__main__':
    unittest.main()
