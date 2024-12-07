import fileinput
import itertools
from dataclasses import dataclass
from enum import Enum
from fileinput import FileInput


class Operator(str, Enum):
    ADD = "+"
    MULTIPLY = "*"
    CONCATENATE = "||"


@dataclass
class Equation:
    target: int
    numbers: list[int]


def evaluate_with_operators(numbers: list[int], operators: list[Operator]) -> int:
    """Evaluates a sequence of numbers with a given list of operators."""
    result = numbers[0]

    # Apply each operator to the running result and the next number in sequence.
    for num, op in zip(numbers[1:], operators):
        if op == Operator.ADD:
            result += num
        elif op == Operator.MULTIPLY:
            result *= num
        elif op == Operator.CONCATENATE:
            result = int(str(result) + str(num))

    return result


def can_produce_target(target: int, numbers: list[int]) -> bool:
    """Checks if target can be produced using +, *, and || operators."""
    num_operator_slots = len(numbers) - 1
    available_operators = list(Operator)

    for operator_combo in itertools.product(available_operators, repeat=num_operator_slots):
        if evaluate_with_operators(numbers, list(operator_combo)) == target:
            return True

    return False


def handler(raw_lines: FileInput) -> int:
    equations: list[Equation] = []

    for raw_line in raw_lines:
        line = raw_line.strip()

        target_str, numbers_str = line.split(":")
        target = int(target_str)
        numbers = [int(x) for x in numbers_str.split()]

        equations.append(Equation(target=target, numbers=numbers))

    total_calibration = 0
    for equation in equations:
        if can_produce_target(equation.target, equation.numbers):
            total_calibration += equation.target

    return total_calibration


if __name__ == "__main__":
    print(handler(fileinput.input()))
