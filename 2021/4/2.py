import sys
from typing import List, Set, TextIO, Tuple


def create_boards(
    raw_numbers: str, raw_boards: List[str]
) -> Tuple[List[int], List[List[Set[int]]]]:
    numbers = [int(num) for num in raw_numbers.split(",")]
    boards = []

    for board in raw_boards:
        rows = [[int(i) for i in row.split()] for row in board.split("\n")]
        boards.append([set(row) for row in rows])
        boards.append([set(col) for col in zip(*rows)])

    return numbers, boards


def get_winning_score(num: int, board: List[Set[int]]) -> int:
    return (sum(sum(group) for group in board) - num) * num


def handler(raw_input: TextIO) -> int:
    raw_numbers, *raw_boards = raw_input.read().split("\n\n")
    numbers, boards = create_boards(raw_numbers, raw_boards)

    for number in numbers:
        for idx, board in enumerate(boards):
            if board is not None:
                if {number} in board:
                    winner = get_winning_score(number, board)
                    boards[idx] = None  # type: ignore
                    if idx % 2:
                        boards[idx - 1] = None  # type: ignore
                    else:
                        boards[idx + 1] = None  # type: ignore
                else:
                    boards[idx] = [group.difference({number}) for group in board]

    return winner


if __name__ == "__main__":
    print(handler(sys.stdin))
