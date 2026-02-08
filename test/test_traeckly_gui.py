import traeckly
import traeckly_gui
import unittest


class Test_parse_command(unittest.TestCase):
    def test_parse_command_found(self):
        """Test parse_command returns the correct command string when found."""
        commands = [
            {"name": "start_trk", "command": "python traeckly.py start {$(task)}"},
            {"name": "stop_trk", "command": "python traeckly.py stop"}
        ]
        tile = {"command": "start_trk", "task": "test_task"}
        result = traeckly_gui.parse_command(commands, tile)
        self.assertEqual(result, "python traeckly.py start test_task")

    def test_parse_command_found_second(self):
        """Test parse_command finds the second command in the list."""
        commands = [
            {"name": "start_trk", "command": "python traeckly.py start {$(task)}"},
            {"name": "stop_trk", "command": "python traeckly.py stop"}
        ]
        tile = {"command": "stop_trk", "task": "test_task"}
        result = traeckly_gui.parse_command(commands, tile)
        self.assertEqual(result, "python traeckly.py stop")

    def test_parse_command_not_found(self):
        """Test parse_command returns empty string when command not found."""
        commands = [
            {"name": "start_trk", "command": "python traeckly.py start {$(task)}"},
            {"name": "stop_trk", "command": "python traeckly.py stop"}
        ]
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
        commands = [
            {"name": "start_trk", "command": "python traeckly.py start {$(task)}"}
        ]
        tile = {"task": "test_task"}
        result = traeckly_gui.parse_command(commands, tile)
        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()
