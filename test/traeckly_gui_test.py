import traeckly
import traeckly_gui
import unittest


class Test_parse_command(unittest.TestCase):
    def test_parse_command_found(self):
        """Test parse_command returns the correct command string when found."""
        config = {
            "commands": [
                {"name": "start_trk", "command": "python traeckly.py start {$(task)}"},
                {"name": "stop_trk", "command": "python traeckly.py stop"}
            ]
        }
        result = traeckly_gui.parse_command(config, "start_trk")
        self.assertEqual(result, "python traeckly.py start {$(task)}")

    def test_parse_command_found_second(self):
        """Test parse_command finds the second command in the list."""
        config = {
            "commands": [
                {"name": "start_trk", "command": "python traeckly.py start {$(task)}"},
                {"name": "stop_trk", "command": "python traeckly.py stop"}
            ]
        }
        result = traeckly_gui.parse_command(config, "stop_trk")
        self.assertEqual(result, "python traeckly.py stop")

    def test_parse_command_not_found(self):
        """Test parse_command returns empty string when command not found."""
        config = {
            "commands": [
                {"name": "start_trk", "command": "python traeckly.py start {$(task)}"},
                {"name": "stop_trk", "command": "python traeckly.py stop"}
            ]
        }
        result = traeckly_gui.parse_command(config, "unknown_command")
        self.assertEqual(result, "")

    def test_parse_command_empty_commands_list(self):
        """Test parse_command with empty commands list."""
        config = {"commands": []}
        result = traeckly_gui.parse_command(config, "any_command")
        self.assertEqual(result, "")

    def test_parse_command_missing_commands_key(self):
        """Test parse_command when commands key is missing from config."""
        config = {}
        result = traeckly_gui.parse_command(config, "any_command")
        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()
