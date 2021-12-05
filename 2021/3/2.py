import fileinput
from fileinput import FileInput
from typing import Dict, List
from enum import Enum


class RatingType(Enum):
    O2 = 1
    CO2 = 2


def rating_system(binary_numbers: List, rating_type: RatingType) -> int:
    comparison_function = int.__ge__ if rating_type == RatingType.O2 else int.__lt__

    for i in range(len(binary_numbers[0])):
        freq_table: Dict[str, List[str]] = {"0": [], "1": []}

        for binary_number in binary_numbers:
            freq_table[binary_number[i]].append(binary_number)

        if (
            len(
                binary_numbers := freq_table[
                    "1"
                    if comparison_function(len(freq_table["1"]), len(freq_table["0"]))
                    else "0"
                ]
            )
            == 1
        ):
            return int(binary_numbers[0], 2)

    return 0


def handler(raw_binary_numbers: FileInput) -> int:
    binary_numbers = [binary_number.strip() for binary_number in raw_binary_numbers]

    o2_rating = rating_system(binary_numbers, RatingType.O2)
    co2_rating = rating_system(binary_numbers, RatingType.CO2)

    return o2_rating * co2_rating


if __name__ == "__main__":
    print(handler(fileinput.input()))
