import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from rover.main import Rover, main


class RoverTests(unittest.TestCase):
    def test_starts_at_origin_facing_north(self):
        self.assertEqual(Rover().position(), (0, 0, "N"))

    def test_turns_cycle_through_all_headings_without_moving(self):
        for command, headings in (("L", "WSEN"), ("R", "ESWN")):
            with self.subTest(command=command):
                rover = Rover()
                for heading in headings:
                    rover.execute(command)
                    self.assertEqual(rover.position(), (0, 0, heading))

    def test_movement_in_each_heading(self):
        cases = (
            ("M", (0, 1, "N")),
            ("RM", (1, 0, "E")),
            ("RRM", (0, -1, "S")),
            ("LM", (-1, 0, "W")),
        )
        for commands, expected in cases:
            with self.subTest(commands=commands):
                rover = Rover()
                for command in commands:
                    rover.execute(command)
                self.assertEqual(rover.position(), expected)

    def test_movements_accumulate_across_turns(self):
        rover = Rover()
        for command in "MMRMLM":
            rover.execute(command)
        self.assertEqual(rover.position(), (1, 3, "N"))

    def test_invalid_command_preserves_state(self):
        rover = Rover()
        rover.execute("L")
        rover.execute("M")

        with self.assertRaisesRegex(ValueError, "^Invalid command: X$"):
            rover.execute("X")

        self.assertEqual(rover.position(), (-1, 0, "W"))


class RoverCLITests(unittest.TestCase):
    def test_normalizes_input_and_preserves_state_between_lines(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["  mr  ", "   ", "m", " q "]) as read:
            with redirect_stdout(output):
                main()

        self.assertEqual(read.call_count, 4)
        self.assertEqual(
            output.getvalue().splitlines(),
            ["(0, 1, 'N')", "(0, 1, 'E')", "(1, 1, 'E')"],
        )

    def test_reports_invalid_commands_and_continues(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["XMQM", "Q"]):
            with redirect_stdout(output):
                main()

        self.assertEqual(
            output.getvalue().splitlines(),
            ["Invalid command: X", "(0, 1, 'N')", "Invalid command: Q", "(0, 2, 'N')"],
        )


if __name__ == "__main__":
    unittest.main()
