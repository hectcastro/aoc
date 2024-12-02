import fileinput
from collections import namedtuple
from fileinput import FileInput

Command = namedtuple("Command", ["direction", "unit"])


def handler(raw_commands: FileInput) -> int:
    commands = [
        Command(*[instruction.strip() for instruction in raw_command.split(" ")]) for raw_command in raw_commands
    ]
    horizontal_position, depth = 0, 0

    for command in commands:
        if command.direction == "forward":
            horizontal_position += int(command.unit)
        elif command.direction == "down":
            depth -= int(command.unit)
        elif command.direction == "up":
            depth += int(command.unit)

    return abs(horizontal_position) * abs(depth)


if __name__ == "__main__":
    print(handler(fileinput.input()))
