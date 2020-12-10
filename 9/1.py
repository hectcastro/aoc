import sys

from typing import List, TextIO

PREAMBLE_SIZE = 25


def is_valid(number: int, preamble: List[int]) -> bool:
    for i in preamble:
        for j in preamble:
            if i + j == number:
                return True
    return False


def handler(raw_port_output: TextIO) -> int:
    port_output: List[int] = []
    for raw_number in raw_port_output.read().splitlines():
        port_output.append(int(raw_number))

    for index, number in enumerate(port_output[PREAMBLE_SIZE:]):
        preamble = port_output[index : (index + PREAMBLE_SIZE)]
        if not is_valid(number, preamble):
            return number

    return 0


if __name__ == "__main__":
    print(handler(sys.stdin))
