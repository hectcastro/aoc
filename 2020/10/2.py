import sys
from collections import defaultdict
from typing import Dict, List, TextIO

ADAPTER_OUTPUT_JOLTAGES: List[int] = []


def handler(raw_output_joltages: TextIO) -> int:
    ADAPTER_OUTPUT_JOLTAGES.append(0)
    for raw_output_joltage in raw_output_joltages.read().splitlines():
        ADAPTER_OUTPUT_JOLTAGES.append(int(raw_output_joltage))

    counter: Dict[int, int] = defaultdict(int)
    counter[0] += 1

    for adapter_joltage in sorted(ADAPTER_OUTPUT_JOLTAGES):
        counter[adapter_joltage] += counter.get(adapter_joltage - 1, 0)
        counter[adapter_joltage] += counter.get(adapter_joltage - 2, 0)
        counter[adapter_joltage] += counter.get(adapter_joltage - 3, 0)

    return counter[max(ADAPTER_OUTPUT_JOLTAGES)]


if __name__ == "__main__":
    print(handler(sys.stdin))
