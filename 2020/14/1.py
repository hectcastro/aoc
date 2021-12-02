import sys
from typing import Dict, TextIO


def handler(raw_program: TextIO) -> int:
    memory: Dict[int, int] = {}
    mask = "X" * 36

    for raw_instruction in raw_program.readlines():
        instruction = raw_instruction.strip()

        if instruction.startswith("mask ="):
            mask = instruction.split(" = ")[1]
            continue

        raw_address, raw_value = instruction.split(" = ")
        address = int(raw_address.lstrip("mem[").rstrip("]"))
        binary_value = bin(int(raw_value))[2:].zfill(36)
        value = ""

        for bit, val in zip(mask, binary_value):
            if bit == "X":
                value += val
            else:
                value += bit

        memory[address] = int(value, 2)

    return sum(memory.values())


if __name__ == "__main__":
    print(handler(sys.stdin))
