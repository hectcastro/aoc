import fileinput
from fileinput import FileInput
from collections import Counter
from typing import List


def handler(raw_binary_numbers: FileInput) -> int:
    binary_numbers = [binary_number.strip() for binary_number in raw_binary_numbers]
    counters: List = [Counter() for _ in range(len(binary_numbers[0]))]

    for binary_number in binary_numbers:
        for i, counter in enumerate(counters):
            counter.update([binary_number[i]])

    gamma = []
    epsilon = []

    for counter in counters:
        most_common = counter.most_common()
        gamma.append(most_common[0][0])
        epsilon.append(most_common[1][0])

    return int("".join(gamma), 2) * int("".join(epsilon), 2)


if __name__ == "__main__":
    print(handler(fileinput.input()))
