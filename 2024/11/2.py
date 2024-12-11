import fileinput
from collections import Counter

BLINKS = 75
MULTIPLIER = 2024


def convert_digits_to_int(digits: list[int]) -> int:
    """Converts a list of digits to an integer, returning 0 for empty lists."""
    return int("".join([str(d) for d in digits]) or "0")


def split_stone_in_half(stone: int) -> tuple[int, int]:
    """Splits an integer into two halves by its digits."""
    digits = []

    # Extract digits from right to left by repeatedly dividing by 10.
    while stone:
        digits.append(stone % 10)
        stone //= 10

    # Reverse digits to get original order.
    digits.reverse()

    mid = len(digits) // 2
    left = convert_digits_to_int(digits[:mid])
    right = convert_digits_to_int(digits[mid:])

    return left, right


def is_even_length_number(stone: int) -> bool:
    """Determines if a number has an even number of digits."""
    return len(str(stone)) % 2 == 0


def handler(raw_lines: fileinput.FileInput) -> int:
    stones = Counter([int(x) for x in next(raw_lines).strip().split()])

    for _ in range(BLINKS):
        new_stones: Counter[int] = Counter()

        for stone, count in stones.items():
            if stone == 0:
                new_stones[1] += count
            elif is_even_length_number(stone):
                left, right = split_stone_in_half(stone)
                new_stones[left] += count
                new_stones[right] += count
            else:
                new_stones[stone * MULTIPLIER] += count

        stones = new_stones

    return sum(stones.values())


if __name__ == "__main__":
    print(handler(fileinput.input()))
