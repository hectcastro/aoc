import fileinput
import operator
from fileinput import FileInput
from typing import Any, Dict

DIRECTIONS = ["N", "E", "S", "W"]


def change_direction(current_direction: str, action: str, value: int) -> Any:
    movement = operator.add

    if action == "L":
        movement = operator.sub
    elif action == "R":
        movement = operator.add

    return DIRECTIONS[
        movement(DIRECTIONS.index(current_direction), (value // 90)) % len(DIRECTIONS)
    ]


def handler(raw_instructions: FileInput) -> int:
    direction = "E"
    distance: Dict[str, int] = dict(zip(DIRECTIONS, [0] * len(DIRECTIONS)))

    for raw_instruction in raw_instructions:
        instruction = raw_instruction.strip()
        action, value = instruction[0], int(instruction[1:])

        if action == "F":
            distance[direction] += value
        elif action in ["N", "S", "E", "W"]:
            distance[action] += value
        elif action in ["L", "R"]:
            direction = change_direction(direction, action, value)

    return abs(distance["E"] - distance["W"]) + (abs(distance["N"] - distance["S"]))


if __name__ == "__main__":
    print(handler(fileinput.input()))
