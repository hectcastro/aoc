import fileinput
from fileinput import FileInput
from typing import Dict

DIRECTIONS: Dict[str, complex] = {
    "N": 0 + 1j,
    "E": 1 + 0j,
    "S": 0 + -1j,
    "W": -1 + 0j,
    "R": 0 - 1j,
    "L": 0 + 1j,
}


def handler(raw_instructions: FileInput) -> int:
    waypoint = 10 + 1j
    position = 0 + 0j

    for raw_instruction in raw_instructions:
        instruction = raw_instruction.strip()
        action, value = instruction[0], int(instruction[1:])

        if action == "F":
            position += waypoint * value
        elif action in ["N", "S", "E", "W"]:
            waypoint += DIRECTIONS[action] * value
        elif action in ["L", "R"]:
            waypoint *= DIRECTIONS[action] ** (value // 90)

    return abs(int(position.real)) + abs(int(position.imag))


if __name__ == "__main__":
    print(handler(fileinput.input()))
