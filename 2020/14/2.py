import sys
from itertools import product
from typing import Dict, List, TextIO


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
        binary_address = bin(address)[2:].zfill(36)

        for bits in map(iter, product("01", repeat=mask.count("X"))):
            new_address: List[str] = []

            for bit, val in zip(mask, binary_address):
                if bit == "X":
                    new_address.append(str(next(bits)))
                elif bit == "0":
                    new_address.append(val)
                elif bit == "1":
                    new_address.append("1")

            memory[int("".join(new_address), 2)] = int(raw_value)

    return sum(memory.values())


if __name__ == "__main__":
    print(handler(sys.stdin))
