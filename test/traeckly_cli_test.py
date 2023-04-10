import traeckly_cli
import unittest   # The test framework

class Test_Traeckli_cli(unittest.TestCase):
    def test_traeckly_cli_argument_parsing(self):
        args = traeckly_cli.parse_arguments(['create', 'Break'])
        self.assertEqual(args['create_task'], 'Break')

        args = traeckly_cli.parse_arguments(['start', 'Task-999'])
        self.assertEqual(args['start_task'], 'Task-999')


if __name__ == '__main__':
    unittest.main()
