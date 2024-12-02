import sys
from typing import Dict, List, TextIO

LIMIT = 30000000


def handler(raw_starting_numbers: TextIO) -> int:
    starting_numbers: List[str] = raw_starting_numbers.read().strip().split(",")
    numbers: List[int] = [int(number) for number in starting_numbers]
    numbers_and_turns: Dict[int, int] = dict(zip(numbers[:-1], range(1, len(numbers) + 1)))
    last_number = numbers[-1]

    for turn in range(len(numbers) + 1, LIMIT + 1):
        if last_number in numbers_and_turns:
            spoken = turn - numbers_and_turns[last_number] - 1
        else:
            spoken = 0

        numbers_and_turns[last_number] = turn - 1
        last_number = spoken

    return last_number


if __name__ == "__main__":
    print(handler(sys.stdin))
