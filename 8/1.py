import sys

from typing import List, TextIO, Tuple

BOOT_CODE: List[Tuple[str, str]] = []
BOOT_CODE_CACHE: List[int] = []
CODE_INDEX = 0
ACCUMULATOR = 0


def execute_instruction(instruction: Tuple[str, str]) -> None:
    global CODE_INDEX
    global ACCUMULATOR

    operation, argument = instruction
    if operation == "nop":
        CODE_INDEX += 1
    elif operation == "acc":
        CODE_INDEX += 1
        ACCUMULATOR += int(argument)
    elif operation == "jmp":
        CODE_INDEX += int(argument)


def handler(boot_code: TextIO) -> int:
    # Load the boot code into a data structure that can be more
    # easily navigated.
    for instruction in boot_code.read().splitlines():
        operation, argument = instruction.split(" ")
        BOOT_CODE.append((operation, argument))

    while True:
        execute_instruction(BOOT_CODE[CODE_INDEX])

        # If we have seen the instruction at this index before,
        # then we should break out of the infinite loop.
        if CODE_INDEX in BOOT_CODE_CACHE:
            break
        BOOT_CODE_CACHE.append(CODE_INDEX)

    return ACCUMULATOR


if __name__ == "__main__":
    print(handler(sys.stdin))
