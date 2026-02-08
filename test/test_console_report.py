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

    def test_create_report(self):
        """Test that create_report runs without errors and produces output."""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.report.create_report(self.data)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        
        # Verify output contains expected elements
        self.assertIn('2026-01-01', output)
        self.assertIn('2026-01-02', output)
        self.assertIn('Task', output)
        self.assertIn('Time spent', output)
        self.assertIn('Break', output)
        self.assertIn('Task-007', output)
        self.assertIn('1:01', output)

    def test_pad_and_concat(self):
        """Test the pad_and_concat method."""
        result = self.report.pad_and_concat('Test', 'Data', 10)
        self.assertEqual(result, 'Test      Data')

    def test_pad_and_concat_exact_length(self):
        """Test pad_and_concat when string is already the target length."""
        result = self.report.pad_and_concat('Test', 'Data', 4)
        self.assertEqual(result, 'TestData')

    def test_pad_and_concat_too_short_length(self):
        """Test pad_and_concat when string is too long for the target length."""
        result = self.report.pad_and_concat('Test', 'Data', 2)
        self.assertEqual(result, 'TeData')


if __name__ == '__main__':
    unittest.main()
