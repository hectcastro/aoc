import sys

from typing import List, TextIO

MAGIC_NUMBER = 50047984


def handler(raw_port_output: TextIO) -> int:
    port_output: List[int] = []
    for raw_number in raw_port_output.read().splitlines():
        port_output.append(int(raw_number))

    for i in range(len(port_output)):
        for j in range(i + 2, len(port_output)):
            contiguous_set = port_output[i:j]
            contiguous_sum = sum(port_output[i:j])

            if contiguous_sum == MAGIC_NUMBER:
                return min(contiguous_set) + max(contiguous_set)
            elif contiguous_sum > MAGIC_NUMBER:
                break

    return 0


if __name__ == "__main__":
    print(handler(sys.stdin))
