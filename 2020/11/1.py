import fileinput
from fileinput import FileInput
from typing import Dict, List, Tuple


def neighbors(x: int, y: int, seat_positions: Dict[Tuple[int, int], str]) -> List[str]:
    adjacent_cells = []

    for row, col in [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y + 1),
        (x - 1, y - 1),
    ]:
        cell = seat_positions.get((row, col), None)
        if cell and cell != ".":
            adjacent_cells.append(cell)

    return adjacent_cells


def handler(raw_seat_positions: FileInput) -> int:
    layouts: List[Dict[Tuple[int, int], str]] = []
    seat_positions: Dict[Tuple[int, int], str] = {}

    for row, raw_seat_position in enumerate(raw_seat_positions):
        for col, status in enumerate(raw_seat_position.strip()):
            seat_positions[(row, col)] = status

    while True:
        new_seat_positions: Dict[Tuple[int, int], str] = {}

        for x, y in seat_positions.keys():  # noqa: PLC0206
            adjacent_cells = neighbors(x, y, seat_positions)
            new_seat_positions[(x, y)] = seat_positions[(x, y)]

            if seat_positions[(x, y)] == "L":
                if all(map(lambda x: x == "L", adjacent_cells)):
                    new_seat_positions[(x, y)] = "#"
            elif seat_positions[(x, y)] == "#":
                if adjacent_cells.count("#") >= 4:
                    new_seat_positions[(x, y)] = "L"

        if len(layouts) > 0 and layouts[-1] == new_seat_positions:
            return list(new_seat_positions.values()).count("#")
        else:
            layouts.append(new_seat_positions)

        seat_positions = new_seat_positions

    return 0


if __name__ == "__main__":
    print(handler(fileinput.input()))
