import fileinput
import re
from collections import namedtuple
from fileinput import FileInput

MulInstruction = namedtuple("MulInstruction", ["pos", "x", "y"])
DoInstruction = namedtuple("DoInstruction", ["pos"])
DontInstruction = namedtuple("DontInstruction", ["pos"])


def handler(raw_instructions: FileInput) -> int:
    pattern_mul = r"mul\((\d{1,3}),(\d{1,3})\)"
    pattern_do = r"do\(\)"
    pattern_dont = r"don\'t\(\)"

    all_instructions = "".join(raw_instructions)

    matches_mul = list(re.finditer(pattern_mul, all_instructions))
    matches_do = list(re.finditer(pattern_do, all_instructions))
    matches_dont = list(re.finditer(pattern_dont, all_instructions))

    instructions = []

    instructions.extend([MulInstruction(pos=m.start(), x=int(m.group(1)), y=int(m.group(2))) for m in matches_mul])
    instructions.extend([DoInstruction(pos=m.start()) for m in matches_do])
    instructions.extend([DontInstruction(pos=m.start()) for m in matches_dont])

    instructions.sort(key=lambda x: x.pos)

    instruction_enabled = True
    total = 0

    for instruction in instructions:
        if isinstance(instruction, DoInstruction):
            instruction_enabled = True
        elif isinstance(instruction, DontInstruction):
            instruction_enabled = False
        elif isinstance(instruction, MulInstruction):
            if instruction_enabled:
                total += instruction.x * instruction.y

    return total


if __name__ == "__main__":
    print(handler(fileinput.input()))
