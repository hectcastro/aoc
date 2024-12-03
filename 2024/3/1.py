import fileinput
import re
from fileinput import FileInput


def handler(raw_instructions: FileInput) -> int:
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

    matches = re.findall(pattern, "".join(raw_instructions))

    total = sum(int(x) * int(y) for x, y in matches)

    return total


if __name__ == "__main__":
    print(handler(fileinput.input()))
