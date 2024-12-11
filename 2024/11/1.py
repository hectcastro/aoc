import fileinput

BLINKS = 25
MULTIPLIER = 2024


def split_stone_in_half(stone: str) -> tuple[int, int]:
    mid = len(stone) // 2
    left = int(stone[:mid].lstrip("0") or "0")
    right = int(stone[mid:].lstrip("0") or "0")

    return left, right


def is_even_length_number(stone: int) -> bool:
    return len(str(stone)) % 2 == 0


def handler(raw_lines: fileinput.FileInput) -> int:
    stones = [int(x) for x in next(raw_lines).strip().split()]

    for _ in range(BLINKS):
        new_stones = []

        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif is_even_length_number(stone):
                left, right = split_stone_in_half(str(stone))
                new_stones.extend([left, right])
            else:
                new_stones.append(stone * MULTIPLIER)

        stones = new_stones

    return len(stones)


if __name__ == "__main__":
    print(handler(fileinput.input()))
