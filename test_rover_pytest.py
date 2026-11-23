from unittest.mock import Mock, call

import pytest

from rover.main import Rover, main


PROMPT = "Enter commands (or Q to quit): "


@pytest.mark.parametrize(
    ("commands", "expected"),
    [
        ("", (0, 0, "N")),
        ("MMM", (0, 3, "N")),
        ("MLMMLMM", (-2, -1, "S")),
        ("MRRMRR", (0, 0, "N")),
    ],
)
def test_command_sequences(commands, expected):
    rover = Rover()
    for command in commands:
        rover.execute(command)

    assert rover.position() == expected


@pytest.mark.parametrize("invalid", ["", "MM", "m", " M ", "Q", None])
def test_execute_rejects_invalid_commands_without_changing_state(invalid):
    rover = Rover()
    rover.execute("R")
    rover.execute("M")

    with pytest.raises(ValueError) as error:
        rover.execute(invalid)

    assert str(error.value) == f"Invalid command: {invalid}"
    assert rover.position() == (1, 0, "E")
    rover.execute("M")
    assert rover.position() == (2, 0, "E")


@pytest.mark.parametrize("quit_input", ["Q", " \tq "])
def test_cli_quits_immediately_without_output(quit_input, monkeypatch, capsys):
    read = Mock(side_effect=[quit_input])
    monkeypatch.setattr("builtins.input", read)

    main()

    read.assert_called_once_with(PROMPT)
    assert capsys.readouterr().out == ""


def test_cli_skips_blank_lines_and_continues_after_each_invalid_character(
    monkeypatch, capsys
):
    read = Mock(side_effect=["", "  mm qq l  ", " m ", "q"])
    monkeypatch.setattr("builtins.input", read)

    main()

    assert read.call_args_list == [call(PROMPT)] * 4
    assert capsys.readouterr().out.splitlines() == [
        "(0, 1, 'N')",
        "(0, 2, 'N')",
        "Invalid command:  ",
        "Invalid command: Q",
        "Invalid command: Q",
        "Invalid command:  ",
        "(0, 2, 'W')",
        "(-1, 2, 'W')",
    ]


@pytest.mark.parametrize("input_failure", [EOFError, KeyboardInterrupt])
def test_cli_propagates_input_failure_without_retry(input_failure, monkeypatch, capsys):
    read = Mock(side_effect=["M", input_failure()])
    monkeypatch.setattr("builtins.input", read)

    with pytest.raises(input_failure):
        main()

    assert read.call_args_list == [call(PROMPT)] * 2
    assert capsys.readouterr().out == "(0, 1, 'N')\n"
