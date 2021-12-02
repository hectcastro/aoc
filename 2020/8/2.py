import copy
import sys
from collections import defaultdict
from typing import Dict, List, TextIO, Tuple

BOOT_CODE: Dict[int, List[Tuple[str, str]]] = defaultdict(list)
BOOT_CODE_CACHE: Dict[int, List[int]] = defaultdict(list)
CODE_INDEX: Dict[int, int] = defaultdict(int)
ACCUMULATOR: Dict[int, int] = defaultdict(int)


def execute_instruction(instruction: Tuple[str, str], index: int) -> None:
    operation, argument = instruction

    if operation == "nop":
        CODE_INDEX[index] += 1
    elif operation == "acc":
        CODE_INDEX[index] += 1
        ACCUMULATOR[index] += int(argument)
    elif operation == "jmp":
        CODE_INDEX[index] += int(argument)


def handler(boot_code: TextIO) -> int:
    template_boot_code: List[Tuple[str, str]] = []

    # Load the boot code into a data structure that can be more
    # easily navigated.
    for inst in boot_code.read().splitlines():
        operation, argument = inst.split(" ")
        template_boot_code.append((operation, argument))

    # Copy the template boot code for each instruction where
    # the operator is nop or jmp.
    for index in range(len(template_boot_code)):
        boot_code_copy = copy.deepcopy(template_boot_code)

        if boot_code_copy[index][0] == "nop":
            boot_code_copy[index] = ("jmp", boot_code_copy[index][1])
        elif boot_code_copy[index][0] == "jmp":
            boot_code_copy[index] = ("nop", boot_code_copy[index][1])
        else:
            BOOT_CODE[index] = []
            continue

        BOOT_CODE[index] = boot_code_copy

    # Go through each index and evaluate all of the instructions
    # with the single corrupt instruction replacement to determine
    # if it completes successfully.
    for index in range(len(template_boot_code)):
        if not BOOT_CODE[index]:
            continue

        while True:
            instruction = BOOT_CODE[index][CODE_INDEX[index]]
            execute_instruction(instruction, index)

            # If we have seen the instruction at this index before,
            # then we should break out of the infinite loop.
            if CODE_INDEX[index] in BOOT_CODE_CACHE[index]:
                break
            BOOT_CODE_CACHE[index].append(CODE_INDEX[index])

            # Ensure that we return the accumulator if it ends up
            # being the last instruction before attempting to loop
            # again.
            if CODE_INDEX[index] == len(template_boot_code):
                return ACCUMULATOR[index]

    return ACCUMULATOR[index]


if __name__ == "__main__":
    print(handler(sys.stdin))
