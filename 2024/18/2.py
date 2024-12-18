import fileinput
from collections import deque
from dataclasses import dataclass

GRID_SIZE = 71
MAX_COORDINATES = 4096

Grid = list[list[bool]]


@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int

    def in_bounds(self, size: int) -> bool:
        return 0 <= self.row < size and 0 <= self.col < size

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.row + other.row, self.col + other.col)

    def __str__(self) -> str:
        return f"({self.col}, {self.row})"


MOVEMENT_DIRECTIONS = [
    Coordinate(0, 1),  # Right
    Coordinate(0, -1),  # Left
    Coordinate(1, 0),  # Down
    Coordinate(-1, 0),  # Up
]

START_POSITION = Coordinate(0, 0)
END_POSITION = Coordinate(GRID_SIZE - 1, GRID_SIZE - 1)


def is_path_available(corrupted_cells: Grid) -> bool:
    """Check if there's still a path from START_POSITION to END_POSITION."""
    if corrupted_cells[START_POSITION.row][START_POSITION.col]:
        return False
    if corrupted_cells[END_POSITION.row][END_POSITION.col]:
        return False

    visited_cells = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    visited_cells[START_POSITION.row][START_POSITION.col] = True

    queue = deque([START_POSITION])
    while queue:
        current = queue.popleft()

        # Found path to end position!
        if current == END_POSITION:
            return True

        # Try moving in each possible direction.
        for direction in MOVEMENT_DIRECTIONS:
            next_pos = current + direction

            # Check if next position is valid.
            if next_pos.in_bounds(GRID_SIZE):
                # Only visit uncorrupted and unvisited cells.
                if not corrupted_cells[next_pos.row][next_pos.col] and not visited_cells[next_pos.row][next_pos.col]:
                    visited_cells[next_pos.row][next_pos.col] = True
                    queue.append(next_pos)

    return False


def handler(raw_lines: fileinput.FileInput) -> Coordinate:
    corrupted_cells: Grid = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    coordinate_count = 0
    for line in raw_lines:
        if coordinate_count >= MAX_COORDINATES:
            break

        col, row = line.strip().split(",")
        coord = Coordinate(row=int(row), col=int(col))

        if coord.in_bounds(GRID_SIZE):
            corrupted_cells[coord.row][coord.col] = True

        # After this byte falls, check if the path is still available.
        if not is_path_available(corrupted_cells):
            # This byte caused the path to be blocked.
            return coord

        coordinate_count += 1

    return Coordinate(-1, -1)


if __name__ == "__main__":
    print(handler(fileinput.input()))
