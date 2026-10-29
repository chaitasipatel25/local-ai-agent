import pytest

from calculator_tool import calculate


def test_addition():
    assert calculate("125 + 37") == "162"


def test_multiplication_and_addition():
    assert calculate("(125 * 8) + 37") == "1037"


def test_division():
    assert calculate("10 / 2") == "5.0"


def test_negative_numbers():
    assert calculate("-5 + 3") == "-2"


@pytest.mark.parametrize(
    "expression",
    [
        "__import__('os').system('echo unsafe')",
        "2 ** 10",
        "unknown_variable",
    ],
)
def test_rejects_unsupported_expressions(expression):
    with pytest.raises((ValueError, TypeError, SyntaxError)):
        calculate(expression)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("1 / 0")
