import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import call, patch

from leetcode299.user_interface import Solution, play_game


class HintTests(unittest.TestCase):
    def test_counts_bulls_and_cows(self):
        cases = (
            ("1231", "1231", "4A0B"),
            ("1231", "9999", "0A0B"),
            ("1231", "3112", "0A4B"),
            ("1807", "7810", "1A3B"),
            ("1123", "0111", "1A1B"),
            ("1231", "1111", "2A0B"),
        )
        solution = Solution()
        for secret, guess, expected in cases:
            with self.subTest(secret=secret, guess=guess):
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(solution.getHint(secret, guess), expected)


class PlayGameTests(unittest.TestCase):
    def play_with_guesses(self, guesses):
        output = io.StringIO()
        with patch("builtins.input", side_effect=guesses) as read:
            with redirect_stdout(output):
                play_game()

        self.assertEqual(read.call_args_list, [call("Enter your guess: ")] * len(guesses))
        # The scoring loop also prints its internal frequency map.
        return [
            line for line in output.getvalue().splitlines()
            if not line.startswith("defaultdict(")
        ]

    def test_winning_guess_ends_game_early(self):
        self.assertEqual(
            self.play_with_guesses(["9999", "1231"]),
            ["0A0B", "4A0B", "Congratulations! You won!"],
        )

    def test_five_incorrect_guesses_reveal_secret(self):
        self.assertEqual(
            self.play_with_guesses(["9999"] * 5),
            ["0A0B"] * 5 + ["Game Over!", "The secret was 1231"],
        )

    def test_correct_guess_on_final_attempt_wins(self):
        self.assertEqual(
            self.play_with_guesses(["9999"] * 4 + ["1231"]),
            ["0A0B"] * 4 + ["4A0B", "Congratulations! You won!"],
        )
