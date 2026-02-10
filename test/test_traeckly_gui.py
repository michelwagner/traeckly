import traeckly
import traeckly_gui
import unittest


class Test_parse_command(unittest.TestCase):
    def test_parse_command_found(self):
        """Test parse_command returns the correct command string when found."""
        commands = {
            "start": "python traeckly.py start {$(task)}",
            "stop": "python traeckly.py stop"
        }
        tile = {"command": "start", "task": "test_task"}
        result = traeckly_gui.parse_command(commands, tile)
        self.assertEqual(result, "python traeckly.py start test_task")

    def test_parse_command_found_second(self):
        """Test parse_command finds the second command in the list."""
        commands = {
            "start": "python traeckly.py start {$(task)}",
            "stop": "python traeckly.py stop"
        }
        tile = {"command": "stop", "task": "test_task"}
        result = traeckly_gui.parse_command(commands, tile)
        self.assertEqual(result, "python traeckly.py stop")

    def test_parse_command_not_found(self):
        """Test parse_command returns empty string when command not found."""
        commands = {
            "start": "python traeckly.py start {$(task)}",
            "stop": "python traeckly.py stop"
        }
        tile = {"command": "unknown_command", "task": "test_task"}
        result = traeckly_gui.parse_command(commands, tile)
        self.assertEqual(result, "")

    def test_parse_command_empty_commands_list(self):
        """Test parse_command with empty commands list."""
        commands = []
        tile = {"command": "any_command", "task": "test_task"}
        result = traeckly_gui.parse_command(commands, tile)
        self.assertEqual(result, "")

    def test_parse_command_missing_command_in_tile(self):
        """Test parse_command when command key is missing from tile."""
        commands = {
            "start": "python traeckly.py start {$(task)}",
        }
        tile = {"task": "test_task"}
        result = traeckly_gui.parse_command(commands, tile)
        self.assertEqual(result, "")


class Test_wrap_text(unittest.TestCase):
    def test_wrap_text_short_text(self):
        """Test that short text is not wrapped."""
        result = traeckly_gui.wrap_text("Short", max_chars=15)
        self.assertEqual(result, "Short")

    def test_wrap_text_empty_string(self):
        """Test that empty string is returned as is."""
        result = traeckly_gui.wrap_text("", max_chars=15)
        self.assertEqual(result, "")

    def test_wrap_text_exact_length(self):
        """Test text that is exactly at max_chars."""
        result = traeckly_gui.wrap_text("Exactly15Chars!", max_chars=15)
        self.assertEqual(result, "Exactly15Chars!")

    def test_wrap_text_wraps_at_whitespace(self):
        """Test that text wraps at whitespace."""
        result = traeckly_gui.wrap_text("This is a longer text", max_chars=15)
        self.assertEqual(result, "This is a\nlonger text")

    def test_wrap_text_wraps_at_hyphen(self):
        """Test that text wraps at hyphens."""
        result = traeckly_gui.wrap_text("Customer-Complaints", max_chars=15)
        self.assertEqual(result, "Customer-\nComplaints")

    def test_wrap_text_multiple_hyphens(self):
        """Test text with multiple hyphens."""
        result = traeckly_gui.wrap_text("t-mass-10-extra", max_chars=10)
        self.assertEqual(result, "t- mass-\n10- extra")

    def test_wrap_text_multiple_lines(self):
        """Test text that requires multiple line breaks."""
        result = traeckly_gui.wrap_text("This is a very long text that needs wrapping", max_chars=15)
        # Should wrap at appropriate boundaries
        lines = result.split('\n')
        self.assertGreater(len(lines), 1)
        for line in lines:
            self.assertLessEqual(len(line), 20)  # Some margin for word boundaries

    def test_wrap_text_single_long_word(self):
        """Test single word longer than max_chars."""
        result = traeckly_gui.wrap_text("VeryLongWordWithoutSpaces", max_chars=10)
        # Single word should be kept on one line even if longer
        self.assertEqual(result, "VeryLongWordWithoutSpaces")

    def test_wrap_text_custom_max_chars(self):
        """Test with different max_chars value."""
        result = traeckly_gui.wrap_text("Short text here", max_chars=5)
        lines = result.split('\n')
        self.assertGreater(len(lines), 1)


if __name__ == '__main__':
    unittest.main()
