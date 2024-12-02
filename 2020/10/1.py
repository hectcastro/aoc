import sys
from collections import defaultdict
from typing import Dict, List, TextIO

JOLTAGE_DIFFS: Dict[int, int] = defaultdict(int)
ADAPTER_OUTPUT_JOLTAGES: List[int] = []
BUILT_IN_ADAPTER_JOLTAGE = 3
ACCEPTED_JOLTAGE_RANGE = 3


def handler(raw_output_joltages: TextIO) -> int:
    for raw_output_joltage in raw_output_joltages.read().splitlines():
        ADAPTER_OUTPUT_JOLTAGES.append(int(raw_output_joltage))

    # Add built-in adapter joltage, which is max of adapters + 3.
    ADAPTER_OUTPUT_JOLTAGES.append(max(ADAPTER_OUTPUT_JOLTAGES) + BUILT_IN_ADAPTER_JOLTAGE)

    outlet_joltage = 0

    for adapter_joltage in sorted(ADAPTER_OUTPUT_JOLTAGES):
        joltage_difference = adapter_joltage - outlet_joltage
        if joltage_difference <= ACCEPTED_JOLTAGE_RANGE:
            outlet_joltage = adapter_joltage
            JOLTAGE_DIFFS[joltage_difference] += 1

    return JOLTAGE_DIFFS[1] * JOLTAGE_DIFFS[3]


if __name__ == "__main__":
    print(handler(sys.stdin))
