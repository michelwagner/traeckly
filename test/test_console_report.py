import unittest
from io import StringIO
import sys
from console_report import ConsoleReport


class TestConsoleReport(unittest.TestCase):
    def setUp(self):
        self.report = ConsoleReport()
        self.data = {
            'from': '2026-01-01',
            'to': '2026-01-02',
            'tasks': [
                ('Break', '1:01'),
                ('Task-007', '0:00'),
                ('Task-123', '0:34'),
                ('Task-777', '0:00'),
                ('Task-778', '2:05')
            ]
        }

    def test_create_report_sum(self):
        """Test that create_report_sum runs without errors and produces output."""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.report.create_report_sum(self.data)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        
        # Verify output contains expected elements
        self.assertIn('2026-01-01', output)
        self.assertIn('2026-01-02', output)
        self.assertIn('Task', output)
        self.assertIn('Time', output)
        self.assertIn('Break', output)
        self.assertIn('Task-007', output)
        self.assertIn('1:01', output)


if __name__ == '__main__':
    unittest.main()
